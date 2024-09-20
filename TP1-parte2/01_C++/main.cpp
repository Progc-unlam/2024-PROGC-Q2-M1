#include <iostream>
#include <list>
#include <thread>
#include <chrono>
#include <vector>
#include <fstream>

using namespace std;

string pathFile;
int numbOfThreads;
vector<string> lines;
vector<int> rpList;

int validarParametros(int numArguementos, char *argumentos[]);
int countLinesOfFile();
list<thread> createThreads(int nLines, int nThreads);
void readLinesFile(int lineIni, int lineFin, int nHilo);

int main(int argc, char *argv[])
{
    int nLines = 0;
    int rt = 0;
    if (!validarParametros(argc, argv))
        return -1;

    auto ini = std::chrono::system_clock::now();
    rpList.resize(numbOfThreads, 0);
    nLines = countLinesOfFile();
    if (nLines < 1)
        return -2;
    list<thread> listThreads = createThreads(nLines, nLines < numbOfThreads ? nLines : numbOfThreads);
    for (auto &hilito : listThreads)
    {
        hilito.join();
    }
    auto fin = std::chrono::system_clock::now();
    for (int i = 0; i < numbOfThreads; i++)
    {
        rt += rpList[i];
    }
    std::chrono::duration<float, std::milli> duration = fin - ini;
    cout << "Duracion de procesamiento en milisegundos" << endl;
    cout << duration.count() << endl;
    cout << "Numero final de caracteres" << endl;
    cout << rt << endl;
    return 0;
}

int validarParametros(int numArguementos, char *argumentos[])
{

    if (numArguementos != 3)
    {
        cout << "Error de parametros" << endl;
        return 0;
    }
    else
    {
        pathFile = argumentos[1];
        numbOfThreads = atoi(argumentos[2]);
        if (numbOfThreads < 0)
        {
            cout << "La cantidad de hilos debe ser mayor a 0" << endl;
            return 0;
        }
    }
    return 1;
}

int countLinesOfFile()
{

    string line;
    int numbersOfLine = 0;

    std::ifstream inputFile(pathFile);
    if (!inputFile)
    {
        cout << "Error al abrir el archivo." << endl;
        return -2;
    }
    while (std::getline(inputFile, line))
    {
        lines.push_back(line);
        numbersOfLine++;
    }
    inputFile.close();
    return numbersOfLine;
}

list<thread> createThreads(int nLines, int nThreads)
{
    list<thread> listThreads;
    int linesForThread = nLines / nThreads;
    int iniLine;
    int endLine;
    for (int i = 0; i < nThreads; i++)
    {
        iniLine = i * linesForThread;
        endLine = (i == nThreads - 1) ? nLines : iniLine + linesForThread;
        listThreads.push_back(std::thread(readLinesFile, iniLine, endLine, i));
    }
    return listThreads;
}

void readLinesFile(int lineIni, int lineFin, int nHilo)
{
    int i;
    string line;
    int rp = 0;
    for (i = lineIni; i < lineFin; i++)
    {
        line = lines[i];
        rp += line.length();
    }
    rpList[nHilo] = rp;
}
