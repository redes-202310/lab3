package taller5;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;

public class ThreadServidor extends Thread{
    private Socket sktCliente = null;
    private int id;

    public ThreadServidor(Socket sktCliente, int id) {
        this.sktCliente = sktCliente;
        this.id = id;
    }

    @Override
    public void run() {
        System.out.println("Inicio de un nuevo thread: " + id);
        try {
//            while (Thread.activeCount() >= 3){
//                System.out.println("Entra en espera el thread "+ id);
//                try {
//                    wait();
//                } catch (InterruptedException e) {
//                    throw new RuntimeException(e);
//                }
//            }
//            notify();

            PrintWriter escritor = new PrintWriter(sktCliente.getOutputStream(), true);
            BufferedReader lector = new BufferedReader(new InputStreamReader(sktCliente.getInputStream()));

            ProtocoloServidor.procesar(lector,escritor);

            escritor.close();
            lector.close();
            sktCliente.close();
        } catch (IOException e){
            e.printStackTrace();
        }
    }
}
