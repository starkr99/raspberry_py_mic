using BixolonAPI;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace PythonConnector
{
    public class PrintLabel
    {

        // Interface Type
        public const int ISerial = 0;
        public const int IParallel = 1;
        public const int IUsb = 2;
        public const int ILan = 3;
        public const int IBluetooth = 5;

        private string GetStatusMsg(int nStatus)
        {
            string errMsg = "";
            switch ((SLCS_ERROR_CODE)nStatus)
            {
                case SLCS_ERROR_CODE.ERR_CODE_NO_ERROR: errMsg = "No Error"; break;
                case SLCS_ERROR_CODE.ERR_CODE_NO_PAPER: errMsg = "Paper Empty"; break;
                case SLCS_ERROR_CODE.ERR_CODE_COVER_OPEN: errMsg = "Cover Open"; break;
                case SLCS_ERROR_CODE.ERR_CODE_CUTTER_JAM: errMsg = "Cutter jammed"; break;
                case SLCS_ERROR_CODE.ERR_CODE_TPH_OVER_HEAT: errMsg = "TPH overheat"; break;
                case SLCS_ERROR_CODE.ERR_CODE_AUTO_SENSING: errMsg = "Gap detection Error (Auto-sensing failure)"; break;
                case SLCS_ERROR_CODE.ERR_CODE_NO_RIBBON: errMsg = "Ribbon End"; break;
                case SLCS_ERROR_CODE.ERR_CODE_BOARD_OVER_HEAT: errMsg = "Board overheat"; break;
                case SLCS_ERROR_CODE.ERR_CODE_MOTOR_OVER_HEAT: errMsg = "Motor overheat"; break;
                case SLCS_ERROR_CODE.ERR_CODE_WAIT_LABEL_TAKEN: errMsg = "Waiting for the label to be taken"; break;
                case SLCS_ERROR_CODE.ERR_CODE_CONNECT: errMsg = "Port open error"; break;
                case SLCS_ERROR_CODE.ERR_CODE_GETNAME: errMsg = "Unknown (or Not supported) printer name"; break;
                case SLCS_ERROR_CODE.ERR_CODE_OFFLINE: errMsg = "Offline (The printer is in an error status)"; break;
                default: errMsg = "Unknown error"; break;
            }
            return errMsg;
        }

        private bool ConnectPrinter()
        {
            string strPort = "";
            int nBaudrate = 115200, nDatabits = 8, nParity = 0, nStopbits = 0;
            int nStatus = (int)SLCS_ERROR_CODE.ERR_CODE_NO_ERROR;

            nStatus = BXLLApi.ConnectPrinterEx(IUsb, strPort, nBaudrate, nDatabits, nParity, nStopbits);

            if (nStatus != (int)SLCS_ERROR_CODE.ERR_CODE_NO_ERROR)
            {
                BXLLApi.DisconnectPrinter();
                MessageBox.Show(GetStatusMsg(nStatus));
                return false;
            }
            return true;
        }

        // byte[] -> String 
        private string ByteToString(byte[] strByte)
        {
            string str = Encoding.Default.GetString(strByte);
            return str;
        }
        // String -> byte[] 
        private byte[] StringToByte(string str)
        {
            byte[] StrByte = Encoding.UTF8.GetBytes(str);
            return StrByte;
        }

        private void SendPrinterSettingCommand()
        {
            // 203 DPI : 1mm is about 7.99 dots
            // 300 DPI : 1mm is about 11.81 dots
            // 600 DPI : 1mm is about 23.62 dots
            int dotsPer1mm = (int)Math.Round((float)BXLLApi.GetPrinterDPI() / 25.4f);
            int nPaper_Width = 60 * dotsPer1mm;
            int nPaper_Height = 50 * dotsPer1mm;
            int nMarginX = 0 * dotsPer1mm;
            int nMarginY = 0 * dotsPer1mm;
            int nSpeed = (int)SLCS_PRINT_SPEED.PRINTER_SETTING_SPEED;
            int nDensity = 14;
            int nOrientation = (int)SLCS_ORIENTATION.BOTTOM2TOP;

            int nSensorType = (int)SLCS_MEDIA_TYPE.GAP;

            //	Clear Buffer of Printer
            BXLLApi.ClearBuffer();

            //	Set Label and Printer
            //BXLLApi.SetConfigOfPrinter(BXLLApi.SPEED_50, 17, BXLLApi.TOP, false, 0, true);
            BXLLApi.SetConfigOfPrinter(nSpeed, nDensity, nOrientation, true, 1, true);

            // Select international character set and code table.To
            BXLLApi.SetCharacterset((int)SLCS_INTERNATIONAL_CHARSET.ICS_USA, (int)SLCS_CODEPAGE.FCP_CP1252);

            /* 
                1 Inch : 25.4mm
                1 mm   :  7.99 Dots (XT5-40, SLP-TX400, SLP-DX420, SLP-DX220, SLP-DL410, SLP-T400, SLP-D420, SLP-D220, SRP-770/770II/770III)
                1 mm   :  7.99 Dots (SPP-L310, SPP-L410, SPP-L3000, SPP-L4000) 
                1 mm   :  7.99 Dots (XD3-40d, XD3-40t, XD5-40d, XD5-40t, XD5-40LCT)
                1 mm   : 11.81 Dots (XT5-43, SLP-TX403, SLP-DX423, SLP-DX223, SLP-DL413, SLP-T403, SLP-D423, SLP-D223)
                1 mm   : 11.81 Dots (XD5-43d, XD5-43t, XD5-43LCT)
                1 mm   : 23.62 Dots (XT5-46)
            */

            BXLLApi.SetPaper(nMarginX, nMarginY, nPaper_Width, nPaper_Height, nSensorType, 0, 2 * dotsPer1mm);

            // Direct thermal
            BXLLApi.PrintDirect("STd", true);
        }
        public void doPrint(int count, string number)
        {
            if (!ConnectPrinter())
                return;


            int multiplier = 1;
            // 203 DPI : 1mm is about 7.99 dots
            // 300 DPI : 1mm is about 11.81 dots
            // 600 DPI : 1mm is about 23.62 dots
            int resolution = BXLLApi.GetPrinterDPI();
            int dotsPer1mm = (int)Math.Round((float)resolution / 25.4f);
            if (resolution >= 600)
                multiplier = 3;


            SendPrinterSettingCommand();

            // Prints string using TrueFont
            //  P1 : Horizontal position (X) [dot]
            //  P2 : Vertical position (Y) [dot]
            //  P3 : Font Name
            //  P4 : Font Size
            //  P5 : Rotation : (0 : 0 degree , 1 : 90 degree, 2 : 180 degree, 3 : 270 degree)
            //  P6 : Italic
            //  P7 : Bold
            //  P8 : Underline
            //  P9 : RLE (Run-length encoding)
            //BXLLApi.PrintTrueFontLib(2 * dotsPer1mm, 5 * dotsPer1mm, "Arial", 14, 0, true, true, false, "Sample Label-1", false);
            BXLLApi.PrintTrueFont(2 * dotsPer1mm, 5 * dotsPer1mm, "Arial", 14, 0, true, true, false, "Coupon", false);

            //	Draw Lines
            BXLLApi.PrintBlock(1 * dotsPer1mm, 10 * dotsPer1mm, 71 * dotsPer1mm, 11 * dotsPer1mm, (int)SLCS_BLOCK_OPTION.LINE_OVER_WRITING, 0);

            //Print string using Vector Font
            //  P1 : Horizontal position (X) [dot]
            //  P2 : Vertical position (Y) [dot]
            //  P3 : Font selection
            //        U: ASCII (1Byte code)
            //        K: KS5601 (2Byte code)
            //        B: BIG5 (2Byte code)
            //        G: GB2312 (2Byte code)
            //        J: Shift-JIS (2Byte code)
            // P4  : Font width (W)[dot]
            // P5  : Font height (H)[dot]
            // P6  : Right-side character spacing [dot], Plus (+)/Minus (-) option can be used. Ex) 5, +3, -10	
            // P7  : Bold
            // P8  : Reverse printing
            // P9  : Text style  (N : Normal, I : Italic)
            // P10 : Rotation (0 ~ 3)
            // P11 : Text Alignment
            //        L: Left
            //        R: Right
            //        C: Center
            // P12 : Text string write direction (0 : left to right, 1 : right to left)
            // P13 : data to print
            // ※ : Third parameter, 'ASCII' must be set if Bixolon printer is SLP-T400, SLP-T403, SRP-770 and SRP-770II.
            //BXLLApi.PrintVectorFont(22, 65, "U", 34, 34, "0", false, false, false, (int)SLCS_ROTATION.ROTATE_0, SLCS_FONT_ALIGNMENT.LEFTALIGN.ToString(), (int)SLCS_FONT_DIRECTION.LEFTTORIGHT, "Sample Label-2");

            BXLLApi.PrintDeviceFont(2 * dotsPer1mm, 12 * dotsPer1mm, (int)SLCS_DEVICE_FONT.ENG_24X38, multiplier, multiplier, (int)SLCS_ROTATION.ROTATE_0, false, "COUPON:");
            BXLLApi.PrintDeviceFont(2 * dotsPer1mm, 17 * dotsPer1mm, (int)SLCS_DEVICE_FONT.ENG_19X30, multiplier, multiplier, (int)SLCS_ROTATION.ROTATE_0, true, $"{count}th coupon");

            BXLLApi.PrintDeviceFont(3 * dotsPer1mm, 36 * dotsPer1mm, (int)SLCS_DEVICE_FONT.ENG_12X20, multiplier, multiplier, (int)SLCS_ROTATION.ROTATE_0, false, $"COUPON CODE : {number}");
            BXLLApi.Print1DBarcode(3 * dotsPer1mm, 40 * dotsPer1mm, (int)SLCS_BARCODE.CODE39, 3 * multiplier, 5 * multiplier, 48 * multiplier, (int)SLCS_ROTATION.ROTATE_0, (int)SLCS_HRI.HRI_NOT_PRINT, number);

            //	Print Command
            BXLLApi.Prints(1, 1);

            // Disconnect printer
            BXLLApi.DisconnectPrinter();
        }
    }
}
