import java.util.concurrent.Semaphore;

public class Bath implements Runnable 
{
    
    private static final int TIME_SLEEP = 3000;
    private static final int BATH_CAPACITY = 2;
    private static final String MAN = "H";
    private static final String WOMAN = "M";
    private static final String DEFAULT_GENDER = "S";

    
    private String gender;
    private int number;

    
    public static int women_counter = 0;
    public static int men_counter = 0;
    
    public static int waiting_women = 0;
    public static int waiting_men = 0;

    public static String current_gender = DEFAULT_GENDER;
    
    public static Semaphore sem_gender_man = new Semaphore(0);
    public static Semaphore sem_gender_woman = new Semaphore(0);
    public static Semaphore sem_access_bath = new Semaphore(BATH_CAPACITY);

    public Bath(String gender, int number)
    {
        this.gender = gender;
        this.number = number;
    }

    public void usarBano() 
    {
        if (Bath.get_current_gender().equals(DEFAULT_GENDER))
        { 
            Bath.set_current_gender(this.gender);
        }

    
        if(!get_current_gender().equals(this.gender))
        {
            
            if (this.gender.equals(MAN))
            {   
                Main.waiting(MAN, this.number);
                Bath.increment_waiting_men();
                P("sem_gender_man");
                Bath.set_current_gender(MAN);
            } else 
            {        
                Main.waiting(WOMAN, this.number);
                Bath.increment_waiting_women();       
                P("sem_gender_woman");        
                Bath.set_current_gender(WOMAN);
            }
        }
        P("acceso_bano");
        Main.enter_to_bath(this.number);
        if (this.gender.equals(MAN)) 
        {
            Bath.increment_men_counter();
        } else 
        {
            Bath.increment_women_counter();
        }
        
        try 
        {
           
            Thread.sleep(TIME_SLEEP); 
        
        } catch (InterruptedException e) 
        {
            e.printStackTrace();
        }
       
        Main.out_of_bath(this.number);
        if (this.gender.equals(MAN)) 
        {
            Bath.decrement_men_counter();
        } else 
        { 
            Bath.decrement_women_counter();
        }
        V("acceso_bano");
        
        if (Bath.get_current_gender().equals(MAN) && get_men_counter() == 0)
        {    
            for (int i = 0; i < Bath.get_waiting_women(); i++)
            {
                V("sem_gender_woman");
            }
            Bath.reset_waiting_women();
            Bath.set_current_gender("S");
        } else if (Bath.get_current_gender().equals(WOMAN) && get_women_counter() == 0) 
        {
            for (int i = 0; i < Bath.get_waiting_men(); i++)
            {
                V("sem_gender_man");
            }
            Bath.reset_waiting_men();
            Bath.set_current_gender("S");
        }
        
    }

    @Override
    public void run() 
    {
        usarBano();
    }

    public void P(String name)
    {
        try {
            if (name.equals("sem_gender_man")) 
            {
                sem_gender_man.acquire();
            }
            else if (name.equals("sem_gender_woman"))
            {
                sem_gender_woman.acquire();
            } else
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
        if (name.equals("sem_gender_man")) 
        {
            sem_gender_man.release();
        }
        else if (name.equals("sem_gender_woman"))
        {
            sem_gender_woman.release();
        } else
        {
            sem_access_bath.release();
        }
    }


    public static synchronized void increment_waiting_women()
    {
        Bath.waiting_women++;
    }

    public static synchronized void reset_waiting_women()
    {
        Bath.waiting_women = 0;
    }

    public static synchronized void increment_waiting_men()
    {
        Bath.waiting_men++;
    }

    public static synchronized void reset_waiting_men()
    {
        Bath.waiting_men = 0;
    }

    public static synchronized int get_waiting_men()
    {
        return Bath.waiting_men;
    }

    public static synchronized int get_waiting_women()
    {
        return Bath.waiting_women;
    }

    public static synchronized int get_men_counter()
    {
        return men_counter;
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

    public static synchronized int get_women_counter()
    {
        return women_counter;
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
    
    public static synchronized void set_current_gender(String gender) 
    {
        current_gender = gender;
    }

    public static synchronized String get_current_gender() 
    {
        return current_gender;
    }
}

