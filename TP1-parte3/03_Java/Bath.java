import java.util.concurrent.Semaphore;

public class Bath implements Runnable 
{
    private static final int TIME_IN_BATH = 5000;
    private static final int TIME_WAITING = 3000;
    private static final int BATH_CAPACITY = 5;
    private static final String MAN = "H";
    private static final String WOMAN = "M";

    private String gender;
    private int number;

    public static int women_counter = 0;
    public static int men_counter = 0;
    public static Semaphore sem_access_bath = new Semaphore(BATH_CAPACITY);

    public Bath(String gender, int number)
    {
        this.gender = gender;
        this.number = number;
    }

    public void use_bath() throws InterruptedException 
    {
        if (this.gender.equals(MAN) && get_women_counter() == 0)
        {
            Main.enter_bath(number);
            Bath.increment_men_counter();

            Thread.sleep(TIME_IN_BATH); 
            
            Main.leave_bath(number);
            Bath.decrement_men_counter();
        } 

        else if (this.gender.equals(WOMAN) && get_men_counter() == 0)
        {
            Main.enter_bath(number);
            Bath.increment_women_counter();
            
            Thread.sleep(TIME_IN_BATH); 
            
            Main.leave_bath(number);
            Bath.decrement_women_counter();
        } else
        { 
            Thread.sleep(TIME_WAITING);
            use_bath();
        }
    }

    public void try_access_bath()
    {
        Main.waiting(gender, number);
        P("access_bath");
        try
        {
            use_bath();
        } catch (Exception e)
        {
            e.printStackTrace();
        }
        V("access_bath");
    }


    @Override
    public void run() 
    {
        try_access_bath();
    }

    public void P(String name)
    {
        try 
        {
            if (name.equals("access_bath")) 
            {
                sem_access_bath.acquire();
            }
            
        } catch(InterruptedException e)
        {
            e.printStackTrace();
        }
        
    }

    public void V(String name)
    {
        if (name.equals("access_bath")) 
        {
            sem_access_bath.release();
        }
    }

    public static synchronized void increment_men_counter()
    {
        men_counter++;
        Main.update_screen();
    }
    
    public static synchronized void decrement_men_counter()
    {
        men_counter--;
        Main.update_screen();
    }
    public static synchronized int get_men_counter()
    {
        return Bath.men_counter;
    }


    public static synchronized void increment_women_counter()
    {
        women_counter++;
        Main.update_screen();
    }

    public static synchronized void decrement_women_counter()
    {
        women_counter--;
        Main.update_screen();
    }

    public static synchronized int get_women_counter()
    {
        return Bath.women_counter;
    }
    
}

