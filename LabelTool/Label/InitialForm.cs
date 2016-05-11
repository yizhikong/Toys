using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Label
{
    public partial class InitialForm : Form
    {
        public InitialForm()
        {
            InitializeComponent();
            select_p_btn.Enabled = false;
            select_c_btn.Enabled = false;
            closeBtn.Enabled = false;
        }

        private void name_box_TextChanged(object sender, EventArgs e)
        {
            if (name_box.Text.Length > 0)
                select_p_btn.Enabled = true;
        }

        private void select_p_btn_Click(object sender, EventArgs e)
        {
            FolderBrowserDialog dialog = new FolderBrowserDialog();
            dialog.SelectedPath = Environment.CurrentDirectory + @".\images";
            dialog.Description = "Select path to load photo";
            if (dialog.ShowDialog() == DialogResult.OK)
            {
                Program.photoPath = dialog.SelectedPath;
                select_c_btn.Enabled = true;
            }
        }

        private void select_c_btn_Click(object sender, EventArgs e)
        {
            FolderBrowserDialog dialog = new FolderBrowserDialog();
            dialog.SelectedPath = Environment.CurrentDirectory + @".\comments";
            dialog.Description = "Select path to load comments";
            if (dialog.ShowDialog() == DialogResult.OK)
            {
                Program.commentPath = dialog.SelectedPath;
                closeBtn.Enabled = true;
            }
        }

        private void closeBtn_Click(object sender, EventArgs e)
        {
            Program.showLabel = !showLabelCheckBox.Checked;
            Program.username = name_box.Text;
            if (Program.showLabel && !Directory.Exists(name_box.Text))
            {
                Directory.CreateDirectory(name_box.Text);
            }
            this.DialogResult = DialogResult.OK;
        }

    }
}
