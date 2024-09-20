import java.util.Scanner;


public class Main {
    public static int vueltas = 1;
    public static void main(String[] args) {

        Scanner scanner = new Scanner(System.in);
        int  i = 0;
        while (true) {

            System.out.println("'H' , 'M' o 'salir':");
            String input = scanner.nextLine();
            
            if (input.equals("H")) {
                Thread acceso_hombre = new Thread(new Bath("H", i));
                acceso_hombre.start();
                i++;
            } else if (input.equals("M")) {
                Thread acceso_mujer = new Thread(new Bath("M", i));
                acceso_mujer.start();
                i++;
            } else if (input.equals("salir")) {
                break;
            } else {
                System.out.println("Entrada no valida.");
            }
        }

        scanner.close();
    }

    /// Este seria el recurso compartido
    public static synchronized void actualizar_pantalla(String genero){
        int contador = 0;
        String str = "Baño: ";
        System.out.println();
        System.out.println("=====================" + Main.vueltas + "=====================");
        if (genero.equals("H")) {
            contador = Bath.contador_hombres;
        } else{
            contador = Bath.contador_mujeres;
        }
        for(int i = 0; i < contador; i++) {
            str += genero + " ";
        }
        System.out.println(str);
        System.out.println("=====================");
        Main.vueltas++;
    }

  

    

}


