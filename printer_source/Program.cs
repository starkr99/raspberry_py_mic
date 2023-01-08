namespace PythonConnector
{
    internal static class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("Running PythonConnector");

            try
            {
                int couponCount = int.Parse(args[0]);
                string couponNumber = args[1];

                Console.WriteLine($"Print couponCount= {couponCount}// couponNumber= {couponNumber}");
                (new PrintLabel()).doPrint(couponCount, couponNumber);
            }catch(Exception er)
            {

            }
        }
    }
}