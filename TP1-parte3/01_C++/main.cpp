#include <fcntl.h>
#include <semaphore.h>

#include <iostream>
#include <list>
#include <thread>
#include <vector>

using namespace std;

#define ERROR_NPARAMETERS -1
#define ERROR_NCLIENTS -2

#define NRESTOKERS 2

int nClients = 0;
vector<sem_t *> semaphores;
sem_t *reponer;

int parametersValidation(int nParamters, char const *paramters[]);
list<thread> createRestockers(int nRestockers);
void reponer(int numb_restocker,sem_t *myInit, sem_t *nextRepo);

int main(int argc, char const *argv[])
{
  int validation = parametersValidation(argc, argv);

  if (validation < 0)
  {
    cout << "Error - " << validation << endl;
    return validation;
  }

  cout << "Good init" << endl;
  cout << "N clients - " << nClients << endl;

  reponer = sem_open("reponer", O_CREAT, 0600, 0);

  list<thread> listRestockers = createRestockers((NRESTOKERS));

  cout << "No empieza aun" << endl;
  sleep(5);
  sem_post(reponer);
  sleep(15);
  sem_post(reponer);

  for (auto &restocker : listRestockers)
  {
    restocker.join();
  }
  for (auto &semaphore : semaphores)
  {
    sem_close(semaphore);
  }

  return 0;
}

int parametersValidation(int nParamters, char const *paramters[])
{
  if (nParamters != 2)
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
  for (int i = 0; i < nRestockers; i++)
  {
    string nameSemaphore = "Número: " + std::to_string(i);
    semaphores.push_back(sem_open(nameSemaphore.c_str(), O_CREAT, 0600, i==0=?1:0));
  }
  for (int i = 0; i < nRestockers; i++)
  {
    restockers.push_back(std::thread(reponer,i+1, semaphores.at(i), semaphores.at(i + 1 < nRestockers ? i + 1 : 0)));
  }

  return restockers;
}

void reponer(int numb_restocker,sem_t *myInit, sem_t *nextRepo)
{
  sem_wait(myInit);
  sem_wait(reponer)
  cout << numb_restocker << " XD" << endl;
  sem_post(nextRepo);
}