using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Label
{
    static class Program
    {
        public static string photoPath = @"D:\code\commicDownload\rankDown";
        public static string commentPath = @"D:\comments";
        public static string username = @"yzkk";
        public static bool showLabel = true;
        
        /// <summary>
        /// The main entry point for the application.
        /// </summary>
        [STAThread]
        static void Main()
        {
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);
            Application.Run(new LabelForm());
        }
    }
}
