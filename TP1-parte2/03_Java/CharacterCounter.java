import java.util.List;

public class CharacterCounter implements Runnable {
	private static final int TIME_SLEEP = 1000;
	private List<String> lines;
	private int rp;
	private int start;
	private int end;
	
	public CharacterCounter(List<String> lines, int start, int end) {
		this.rp = 0;
		this.lines = lines;
		this.start = start;
		this.end = end;
	}
	
	public int getRp(){
		return this.rp;
	}

	public void count_characters() {
		int count = 0;
		String line = "";

		// Itero lineas
		for (int i = this.start; i < this.end; i++){	
			line = this.lines.get(i);
			// Itero caracteres de la linea
			for (int j = 0; j < line.length(); j++){		
				count++;
			}
		}
		try{
			Thread.sleep(TIME_SLEEP);
		} catch(InterruptedException e){
			e.printStackTrace();
		}
		
		this.rp = count;
	}

	@Override
	public void run(){
		count_characters();
		
	}
}
