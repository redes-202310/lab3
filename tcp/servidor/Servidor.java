package taller5;

import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;

public class Servidor {
    public static final int PUERTO = 3400;

    public static void main(String[] args) throws IOException {
        int numeroThreads = 0;
        ServerSocket ss = null;
        boolean continuar = true;

        System.out.println("Main server ...");

        try {
            ss = new ServerSocket(PUERTO);
        } catch (IOException e){
            System.err.println("No se pudo crear el socket en el puerto: " + PUERTO);
            System.exit(-1);
        }

        while (continuar){
            Socket socket = ss.accept();
            ThreadServidor thread = new ThreadServidor(socket, numeroThreads);
            numeroThreads ++;
            thread.start();

        }
        ss.close();
    }
}
