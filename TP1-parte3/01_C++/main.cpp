#include <fcntl.h>
#include <semaphore.h>
#include <unistd.h>

#include <cstdlib>
#include <iostream>
#include <list>
#include <mutex>
#include <thread>
#include <vector>

using namespace std;

#define ERROR_NPARAMETERS -1
#define ERROR_NCLIENTS -2

#define NADMITTED_PARAMTERS 2
#define NRESTOKERS 2
#define MAX_BUY 2
#define MIN_BUY 1

int nClients = 0;
vector<sem_t *> semaphores;
sem_t *reponerS;
sem_t *waitRestock;
mutex gondolaAccesMutex;
mutex waitingArea;
int productCount = 10;
bool noMoreClients = false;

int parametersValidation(int nParamters, char const *paramters[]);
list<thread> createRestockers(int nRestockers);
void reponer(int numb_restocker, sem_t *myInit, sem_t *nextRepo);
list<thread> createClients(int nClients);
void comprar(int order);

int main(int argc, char const *argv[])
{
  int validation = parametersValidation(argc, argv);

  if (validation < 0)
  {
    cout << "Error - " << validation << endl;
    return validation;
  }

  cout << "N clients - " << nClients << endl;

  reponerS = sem_open("reponer", O_CREAT, 0600, 0);
  waitRestock = sem_open("esperar", O_CREAT, 0600, 0);
  waitingArea.lock();
  list<thread> listRestockers = createRestockers((NRESTOKERS));
  list<thread> listClients = createClients(nClients);

  waitingArea.unlock();
  for (auto &client : listClients)
  {
    client.join();
  }
  cout << "Close SuperMarket" << endl;
  noMoreClients = true;
  for (auto &restocker : listRestockers)
  {
    restocker.join();
  }
  int indxNameSemaphore = 0;
  string nameSemaphoreClose;
  for (auto &semaphore : semaphores)
  {
    nameSemaphoreClose = "Número: " + std::to_string(indxNameSemaphore);
    sem_close(semaphore);
    sem_unlink(nameSemaphoreClose.c_str());
    indxNameSemaphore++;
  }
  sem_close(reponerS);
  sem_close(waitRestock);
  sem_unlink("reponer");
  sem_unlink("esperar");
  return 0;
}

int parametersValidation(int nParamters, char const *paramters[])
{
  if (nParamters != NADMITTED_PARAMTERS)
  {
    return ERROR_NPARAMETERS;
  }
  else
  {
    nClients = atoi(paramters[1]);
    if (nClients < 0)
    {
      return ERROR_NCLIENTS;
    }
  }
  return 0;
}

list<thread> createRestockers(int nRestockers)
{
  list<thread> restockers;
  string nameSemaphore;
  for (int i = 0; i < nRestockers; i++)
  {
    nameSemaphore = "Número: " + std::to_string(i);
    semaphores.push_back(sem_open(nameSemaphore.c_str(), O_CREAT, 0600, i == 0 ? 1 : 0));
  }
  for (int i = 0; i < nRestockers; i++)
  {
    restockers.push_back(std::thread(reponer, i + 1, semaphores.at(i), semaphores.at(i + 1 < nRestockers ? i + 1 : 0)));
  }

  return restockers;
}

void reponer(int numb_restocker, sem_t *myInit, sem_t *nextRepo)
{
  while (1)
  {
    while (sem_trywait(myInit) != 0)
    {
      sleep(5);
      if (noMoreClients == true) return;
    }
    while (sem_trywait(reponerS) != 0)
    {
      sleep(1);
      if (noMoreClients == true) return;
    }
    cout << "Restocker N°" << numb_restocker << " restocking" << endl;
    gondolaAccesMutex.lock();
    productCount = 10;
    gondolaAccesMutex.unlock();
    sem_post(nextRepo);
    sem_post(waitRestock);
  }
}

list<thread> createClients(int nClients)
{
  list<thread> clients;
  int nRand;
  for (int i = 0; i < nClients; i++)
  {
    nRand = MIN_BUY + (std::rand() % (MAX_BUY - MIN_BUY + 1));
    clients.push_back(std::thread(comprar, nRand));
  }

  return clients;
}

void comprar(int order)
{
  waitingArea.lock();
  gondolaAccesMutex.lock();
  cout << " I want " << order << " products..." << endl;

  if (productCount - order < 0)
  {
    cout << "   - I'll wait for " << order << " more." << endl;
    gondolaAccesMutex.unlock();
    sem_post(reponerS);
    sem_wait(waitRestock);
    gondolaAccesMutex.lock();
  }
  productCount -= order;
  cout << " Thanks :D " << endl;
  gondolaAccesMutex.unlock();
  waitingArea.unlock();
}