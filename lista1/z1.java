// Piotr Grabowski
// 2012
// ETO Zestaw 1

import java.io.*;

class MyProgram {

    static boolean is_prime(int value) {
        boolean prime = true;
        int counter = 3;
        int val_square = (int) Math.sqrt(value);
      
        if (value == 1)
            prime = false;
        else if (value != 2)
            prime = (value % 2) == 1;
        while (prime && counter <= val_square) { 
            if ( (value % counter) == 0 ) 
                prime = false; 
            counter += 2; 
        }

        return prime;
    }

    static int factorial(int value) {
        int fact = 1;
        for (int i = 1; i <= value; i++)
            fact *= i;
        return fact;
    }

    static int get_number() {
        String input = new String();
        BufferedReader in = new BufferedReader(new InputStreamReader(System.in));
        int value;
        do {
            System.out.print("Enter a positive integer: ");
            try { 
                input = in.readLine(); 
            } catch (IOException e) {};
            value = Integer.parseInt(input);
        } while (value <= 0);
        return value;
    }

    static int get_int_number() {
        String input = new String();
        BufferedReader in = new BufferedReader(new InputStreamReader(System.in));
        System.out.print("Enter a positive integer: ");
        
        try { 
            input = in.readLine(); 
        } catch (IOException e) {};
        
        int value = Integer.parseInt(input);
        
        return value;

    }

    static void print_primes(int value) {
        for (int i = 1; i <= value; ++i)
            if (is_prime(i))
                System.out.print(i + ", ");
    }

    static int max(int a, int b) {
        return (a>=b) ? a : b;
    }
    
    static int min(int a, int b) {
        return (a<=b) ? a : b;
    }

    public static void main(String args[]) {
        BufferedReader in = new BufferedReader(new InputStreamReader(System.in));
        char menu_choice; 
        do {
        
            System.out.println();
            System.out.println("What do you want to do?");
            System.out.println("  1: Prime test");
            System.out.println("  2: Calculate a factorial");
            System.out.println("  3: Print all primes respective to x");
            System.out.println("  4: Max of two integers");
            System.out.println("  5: Min of two integers");
            System.out.println("  0: Exit from  program");
            System.out.print("Your choice: ");
        
            String input = new String();
        
            try {
                input = in.readLine();
            }
            catch (IOException e) {};
        
            menu_choice = input.charAt(0);
            System.out.println("Menu choice = " + menu_choice);
        
            int number, a,b;
            switch (menu_choice) {
                case '1':
                    number = get_number();

                    if (is_prime(number))
                        System.out.println(number + " is prime.");
                    else
                        System.out.println(number + " is not prime.");
                    break;

                case '2':
                    number = get_number();
                    System.out.println("The factorial of " + number + " is " + factorial(number));
                    break;
                case '3':
                    number = get_number();
                    System.out.print("All primes respective to " + number + ": ");
                    print_primes(number);
                    System.out.println();
                    break;
                case '4':
                    a = get_int_number();
                    b = get_int_number();
                    System.out.println("Max of " + a + " and " + b + " is: "  + max(a,b));

                    break;
                case '5':
                    a = get_int_number();
                    b = get_int_number();
                    System.out.println("Min of " + a + " and " + b +" is: "  + min(a,b));
                    break;
                case '0' :
                    break;
                default:
                    System.out.println("Invalid choice!");
            }
        
        } while (menu_choice != '0');
        
    }
    
}
