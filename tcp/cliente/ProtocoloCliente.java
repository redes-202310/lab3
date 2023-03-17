package Cliente;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.PrintWriter;

public class ProtocoloCliente {


    public static void procesar(BufferedReader stdIn, BufferedReader pIn, PrintWriter pOut) throws IOException {
        String fromServer;
        String fromUser;

        boolean ejecutar = true;

        while (ejecutar) {
            System.out.println("Escriba el mensaje para enviar: ");
            fromUser = stdIn.readLine();

            if(fromUser != null) {
                System.out.println("El usuario escribió: " + fromUser);
                if(fromUser.equalsIgnoreCase("OK")) {
                    ejecutar = false;
                }

                pOut.println(fromUser);
            }

            if((fromServer = pIn.readLine()) != null) {
                System.out.println("Respuesta del servidor: " + fromServer);
            }
        }
    }
}
