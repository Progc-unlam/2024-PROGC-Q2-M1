import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class MainProcess 
{
	public static final int TIME_VERIFICATION = 4000;

	public static void main(String[] args) throws IOException, InterruptedException 
	{
		ProcessHandle process = ProcessHandle.current();
		long pid = process.pid();
	    long ppid = process.parent().get().pid();
	    String processName="";

	    if (args.length == 0) 
		{
	    	processName = "A";
	    } 
		else 
		{
	    	processName = args[0];
	    }
	    System.out.println("Proceso: "+ processName + " PID: " + pid + " PID Padre: " + ppid);
	    
	    List<Process> childs = new ArrayList<>();
	    
	    if (processName.equals("A")) 
		{
	    	childs.add(createProcess("B"));
	    }
	    else if (processName.equals("B")) 
		{
	    	childs.add(createProcess("C"));
	    	childs.add(createProcess("D"));
	    }
	    else if (processName.equals("C")) 
		{
	    	childs.add(createProcess("E"));
	    }
	    else if (processName.equals("E")) 
		{
	    	childs.add(createProcess("H"));
	    	childs.add(createProcess("I"));
	    }
	    else if (processName.equals("D")) 
		{
	    	childs.add(createProcess("F"));
	    	childs.add(createProcess("G"));
	    } 
	
		
	    Thread.sleep(TIME_VERIFICATION);	
		
	    
	    for(Process child : childs) 
		{
	    	child.waitFor();  

	    }
	}
	
	private static Process createProcess(String processName) throws IOException, InterruptedException 
	{
		ProcessBuilder pb = new ProcessBuilder("java", "MainProcess.java", processName);
		pb.inheritIO();
		Process process = pb.start();
		return process;
	}
}
