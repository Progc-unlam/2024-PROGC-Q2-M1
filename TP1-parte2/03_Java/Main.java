import java.util.List;
import java.util.ArrayList;
import java.util.Scanner;
import java.io.File;



public class Main 
{
	public static void main(String[] args) 
    {
        
        if (!validate_parameters(args)) 
        {
            return;
        }
        
		int total_threads = Integer.parseInt(args[1]);
        String file_path = args[0];

        
        List<String> lines = new ArrayList<>();
        read_file(file_path, lines);

        
        long t1 = System.currentTimeMillis();
        int rt = execute_counter(lines, total_threads);
        long t2 = System.currentTimeMillis();

        long tt = (t2 - t1);

        System.out.println("Total: " + rt + " calculado en: " + tt + "ms");
	}

    public static boolean validate_parameters(String[] parameters) 
    {
        if (parameters.length > 2 || parameters.length < 1)
        {
            System.out.println("Cantidad de parametros incorrecto.");
            return false;
        }

        File file = new File(parameters[0]);
        if (!file.exists() || !file.isFile())
        {
            System.out.println("El primer parametro debe ser un archivo.");
            return false;
        }
        
        int total_threads;
        try
        {
            total_threads = Integer.parseInt(parameters[1]);
        } 
        catch (NumberFormatException e) 
        {
            System.out.println("El 2do parametro tiene que ser un numero.");
            return false;
        }
        if (total_threads < 1) 
        {
			System.out.println("La cantidad de threads tiene que ser igual o mayor a 1.");
			return false;
		}

        return true;
    }
    
	private static void read_file(String name, List<String> lines) 
    {
		File fp = null;
		Scanner sc = null;
        String line = "";

		try
        {
			fp = new File(name);
			sc = new Scanner(fp);
			
			while (sc.hasNextLine()) 
            {
				line = sc.nextLine();
                if(!line.trim().isEmpty()) 
                {
                    lines.add(line);
                }
				
			}
		} catch( Exception e)
        {
			e.printStackTrace();
		} 
        finally 
        {
			sc.close();
		}
	}
    private static int execute_counter(List<String> lines, int total_threads)
    {
        
        int total_lines = lines.size();

        
        if (total_threads > total_lines) 
        {   
            total_threads = total_lines;
        }
		
		Thread[] threads = new Thread[total_threads];
		CharacterCounter[] counters = new CharacterCounter[total_threads];
		
		int lines_per_thread = (total_lines/total_threads);
        int start = 0;
        int end = 0;
		for (int i = 0; i < total_threads; i++ ) 
        {
			start = i * lines_per_thread;
            end = (i == total_threads -1)? total_lines : start + lines_per_thread;
            counters[i] = new CharacterCounter(lines, start, end);
            threads[i] = new Thread(counters[i]);
            threads[i].start();
            System.out.println("Hilo: " + i + " ejecutando: " + start + " hasta " + end);
		}

        
        try
        {
            for (int i = 0; i < total_threads; i++) 
            {
                threads[i].join();
            }
        } 
        catch (InterruptedException e) 
        {
            e.printStackTrace();
        }
        
        
        int rt = 0;
        for (CharacterCounter counter : counters) 
        {
            rt += counter.getRp();
        }


        return rt;
    }
}
    

