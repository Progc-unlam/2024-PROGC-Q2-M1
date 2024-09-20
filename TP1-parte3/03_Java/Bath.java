import java.util.concurrent.Semaphore;

public class Bath implements Runnable {

    // ERROR NO VUELVEN A SUBIR EL VALOR DEL SEMAFORO SEM_ACCESO_BANO
    // solucion: no hacerlo estatico, posible deadlock al usar syncro

    // ERROR: ejecutar H-H-M-M con cap=2
    // al no usar semaforo y solo el while, hace que solo ejecute 1 M
    // TODO: solucion: el while tiene que ser un semaforo pero nose 
    private static final int TIME_SLEEP = 3000;
    private static final int CAP_BANO = 2;


    public static int contador_mujeres = 0;
    public static int contador_hombres = 0;
    
    public static int espera_mujeres = 0;
    public static int espera_hombres = 0;

    public static String genero_actual = "S";
    
    public static Semaphore sem_genero_h = new Semaphore(0);
    public static Semaphore sem_genero_m = new Semaphore(0);
    public static Semaphore sem_acceso_bano = new Semaphore(CAP_BANO);

    private String genero;
    private int nombre;

    public Bath(String genero, int nombre ){
        this.genero = genero;
        this.nombre = nombre;

    }

    public void usarBano() {

        if (genero_actual.equals("S")){ //TODO:sincronizar
            set_genero(this.genero);
        }

        /// si el que entra, no es del genero correcto, entonces no le dejo pasar

        if(!genero_actual.equals(this.genero)){

            if (this.genero.equals("H")){   /// la fila es de mujeres y entra un hombre
                P("sem_genero_h");
                set_genero("H");
            } else {        
                System.out.println("entro mujer a espera");    
                espera_mujeres++;    
                P("sem_genero_m");          /// problema si vienen varias mujeres, y quedan bloqueadas aca, entonces rompe porque solo se libera 1 vez al llegar hombres a 0
                                                /// contador de mujeres en espera que se ejecute cuando se vacia, como mucho tiene que ser la cap del bano
                                                    //// SOLUCIONADO: ahora el problema es que si ejecuta dos veces M en espera, al liberar borra todos POSIBLMENTE CORRECTO YA QUE DEPENDE DE LA VELOCIDAD EN QUE INGRESEN, PUEDEN SALIR AL MISMO TIEMPO
                System.out.println("mujer salio de espera"); 
                set_genero("M");
            }
        }
        P("acceso_bano");

        if (this.genero.equals("H")) {
            incrementar_contador_hombres();
        } else {
            incrementar_contador_mujeres();
        }

        
        try {
            Thread.sleep(TIME_SLEEP); // Simula el tiempo que el hilo esta usando el baño ////

        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        if (this.genero.equals("H")) {
            decrementar_contador_hombres();
        } else {
            decrementar_contador_mujeres();
        }

       

        // System.out.println("Salio del bano: " + this.nombre);
        
        V("acceso_bano");
        System.out.println("libero bano");
        if (genero_actual.equals("H") && contador_hombres == 0){    // si la fila es de hombres y se vacio, entonces permito entrar mujeres|hombres y el genero vuelve a default
           
            System.out.println("espera mujeres:" + espera_mujeres);
            for (int i = 0; i < espera_mujeres; i++){
                V("sem_genero_m");
            }
            espera_mujeres = 0;
            set_genero("S");
        } else if (genero_actual.equals("M") && contador_mujeres == 0) {
            
            for (int i = 0; i < espera_hombres; i++){
                V("sem_genero_h");
            }
            
            espera_hombres = 0;
            
            set_genero("S");
        }

    }

    @Override
    public void run() {
        usarBano();
    }

    public void P(String name){
        try {
            if (name.equals("sem_genero_h")) {
                sem_genero_h.acquire();
            }
            else if (name.equals("sem_genero_m")){
                sem_genero_m.acquire();
            } else{
                sem_acceso_bano.acquire();
            }
            
        } catch(InterruptedException e){
            e.printStackTrace();
        }
        
    }

    public void V(String name){
        if (name.equals("sem_genero_h")) {
            sem_genero_h.release();
        }
        else if (name.equals("sem_genero_m")){
            sem_genero_m.release();
        } else{
            sem_acceso_bano.release();
        }
    }

    public static synchronized int get_contador_hombres(){
        return contador_hombres;
    }
    public static synchronized void incrementar_contador_hombres(){
        contador_hombres++;
        Main.actualizar_pantalla("H");
    }
    // syncro solo se hace a nivel objeto, pero si se utiliza static, entonces es a nivel clase
    public static synchronized void decrementar_contador_hombres(){
        contador_hombres--;
        Main.actualizar_pantalla("H");
    }

    public static synchronized int get_contador_mujeres(){
        return contador_mujeres;
    }
    public static synchronized void incrementar_contador_mujeres(){
        contador_mujeres++;
        Main.actualizar_pantalla("M");
    }
    public static synchronized void decrementar_contador_mujeres(){
        contador_mujeres--;
        Main.actualizar_pantalla("M");
    }
    
    public static synchronized void set_genero(String genero) {
        genero_actual = genero;
    }
    public static synchronized String get_genero() {
        return genero_actual;
    }
}

