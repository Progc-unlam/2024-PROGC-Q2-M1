import java.util.concurrent.Semaphore;

public class Bath implements Runnable 
{
    /* Constantes */
    private static final int TIME_IN_BATH = 5000;
    private static final int TIME_WAITING = 3000;
    private static final int BATH_CAPACITY = 5;
    private static final String MAN = "H";
    private static final String WOMAN = "M";


    /* Variables propias de cada persona */
    private String gender;
    private int number;

    /* Recursos compartidos */
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
        /* Si un hombre quiere entrar y no hay mujeres en el baño, entonces pasa */
        if (this.gender.equals(MAN) && get_women_counter() == 0)
        {
            /* Si es el primer hombre, entonces bloqueo el acceso a mujeres */
            Main.enter_bath(number);

            /* Dibujo un hombre en pantalla */
            Bath.increment_men_counter();

            /* Simula el tiempo que el hilo esta usando el baño */
            Thread.sleep(TIME_IN_BATH); 
            
            Main.leave_bath(number);
            /* Borro al hombre en pantalla */
            Bath.decrement_men_counter();
          
           
        } 
        /* Entra mujer y contador de hombres debe estar en 0 */
        else if (this.gender.equals(WOMAN) && get_men_counter() == 0)
        {
            Main.enter_bath(number);
            
            /* Dibujo una mujer en pantalla */
            Bath.increment_women_counter();
            
            /* Simula el tiempo que el hilo esta usando el baño */
            Thread.sleep(TIME_IN_BATH); 
            
            /* Se va y actualiza la pantalla */
            Main.leave_bath(number);
            Bath.decrement_women_counter();
        } else
        { 
            /* Si no pudo ingresar sea hombre o mujer, se va un rato y vuelve a intentar (pero con su lugar reservado para evitar inanicion) */
            Thread.sleep(TIME_WAITING);
            use_bath();
        }
    }

    public void try_access_bath(){
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

