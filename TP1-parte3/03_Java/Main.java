import java.util.Scanner;


public class Main 
{
    
    private static final String MAN = "H";
    private static final String WOMAN = "M";

    
    public static int access_counter = 1;
    public static void main(String[] args) 
    {
        System.out.println("Este programa simula el acceso a un baño donde solo hombres entran o solo mujeres.");
        System.out.println("Ingrese 'H' para simular el ingreso de un hombre");
        System.out.println("Ingrese 'M' para simular el ingreso de una mujer\nPara finalizar, ingrese 'salir'");

        Scanner scanner = new Scanner(System.in);
        int i = 1;

        while (true) 
        {
            System.out.println("'H' , 'M' o 'salir':");
            String input = scanner.nextLine();
            
            if (input.equals(MAN)) 
            {
                Thread man_access = new Thread(new Bath(MAN, i));
                man_access.start();
                i++;
            } 
            else if (input.equals(WOMAN)) 
            {
                Thread woman_access = new Thread(new Bath(WOMAN, i));
                woman_access.start();
                i++;
            } 
            else if (input.equals("salir")) 
            {
                break;
            } 
            else 
            {
                System.out.println("Entrada no valida.");
            }
        }

        scanner.close();
    }

    
    public static synchronized void update_screen()
    {
        int counter = 0;
        String gender = "";
        String out = "Baño: ";
        System.out.println();
        System.out.println("=====================" + Main.access_counter + "=====================");

        int man_counter = Bath.get_men_counter();
        int woman_counter = Bath.get_women_counter();

        counter = man_counter != 0 ? man_counter : woman_counter;
        gender = man_counter !=0 ? MAN : WOMAN;

        for(int i = 0; i < counter; i++) 
        {
            out += gender + " ";
        }
        System.out.println(out);
        System.out.println("=====================");
        Main.access_counter++;
    }

    public static synchronized void enter_to_bath(int number)
    {
        System.out.println("Persona: " + number + " ingresando");
    }

    public static synchronized void out_of_bath(int number)
    {
        System.out.println("Persona: " + number + " saliendo");
    }

    public static synchronized void waiting(String gender, int number)
    {
        System.out.println("Persona: " + number + "de genero: " + gender + " esta esperando");
    }
}


