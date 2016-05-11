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
    public partial class LabelForm : Form
    {
        private string[] photoNames;
        private List<List<string>> commentsOfPhoto;
        private System.Windows.Forms.Label[] commentLabels;
        private System.Windows.Forms.FlowLayoutPanel[] flows;
        private System.Windows.Forms.RadioButton[] points;
        Button NextBtn;
        Button PreviousBtn;
        private int[] marks;
        private int labelAmount = 5;
        private const int SHOW_COMMENTS_COUNT = 60;

        
        private int pos;
        public LabelForm()
        {
            InitializeComponent();
            // delegate, when a radio button is checkek, check all the radio buttons to
            // judge whether we should enable the next button
            pos = 0;
            label32.Visible = false;

            NextBtn = new Button();
            NextBtn.Margin = new System.Windows.Forms.Padding(3, 3, 3, 30);
            NextBtn.Size = new System.Drawing.Size(75, 23);
            NextBtn.Text = "Next";
            NextBtn.Click += Next_Click;
            PreviousBtn = new Button();
            PreviousBtn.Margin = new System.Windows.Forms.Padding(3, 3, 3, 30);
            PreviousBtn.Size = new System.Drawing.Size(75, 23);
            PreviousBtn.Text = "Previous";
            PreviousBtn.Click += button1_Click;
            PreviousBtn.Visible = true;
            
            //if (Program.showLabel)
            //{
            //    PreviousBtn.Visible = false;
            //}
        }

        protected override void OnLoad(EventArgs e)
        {
            this.Hide();
            InitialForm initialForm = new InitialForm();
            DialogResult res = initialForm.ShowDialog();
            if (res == DialogResult.OK)
            {
                if (Program.showLabel)
                {
                    // initial
                    pos = Directory.GetFiles(Program.username).Length;
                    PreviousBtn.Visible = false;
                }
                photoNames = Directory.GetFiles(Program.photoPath);
                // filt photo names
                List<string> pns = new List<string>();
                for (int i = 0; i < photoNames.Length; i++ )
                {
                    if (photoNames[i].EndsWith("jpg") || photoNames[i].EndsWith("png"))
                        pns.Add(photoNames[i]);
                }
                photoNames = pns.ToArray();
                bool loadRes = loadMsg();
                if (loadRes)
                    updateMsg();
                this.Show();
            }
            else
            {
                this.Close();
                return;
            }
        }

        // get the comments by the photo name
        List<string> getCommentsOfPhoto(string photoname)
        {
            string[] splitName = photoname.Split('\\');
            string cmtFile = Program.commentPath + "\\" + splitName[splitName.Length - 1] + ".txt";
            List<string> comments = new List<string>();
            if (File.Exists(cmtFile))
            {
                StreamReader sr = new StreamReader(cmtFile);
                string line;
                while ((line = sr.ReadLine()) != null && comments.Count < SHOW_COMMENTS_COUNT)
                {
                    //comments.Add(line.Trim().Split('\t')[1]);
                    comments.Add(line.Trim());  // for comments without scores
                }
                sr.Close();
                // momo
                return comments;
            }
            else
            {
                return comments;
            }
        }

        // load comments of all photo
        bool loadMsg()
        {
            if (Program.showLabel)
            {
                PreviousBtn.Visible = false;
            }

            if (photoNames != null && photoNames.Length > 0)
            {
                commentsOfPhoto = new List<List<string>>();
                for (int i = 0; i < photoNames.Length; i++)
                {
                    commentsOfPhoto.Add(getCommentsOfPhoto(photoNames[i]));
                }
                return true;
            }
            return false;
        }

        // update the comments and marks in the form
        void updateMsg()
        {
            if (Program.showLabel)
            {
                PreviousBtn.Visible = false;
            }
            string filename = System.IO.Path.GetFileName(photoNames[pos]);
            percent_label.Text = "Process : " + (pos + 1) + "/" + photoNames.Length + "     " + filename;
            // intial controls
            rightLayout.Controls.Clear();
            commentLabels = new System.Windows.Forms.Label[commentsOfPhoto[pos].Count];
            flows = new FlowLayoutPanel[commentsOfPhoto[pos].Count];
            marks = new int[commentsOfPhoto[pos].Count];
            points = new RadioButton[commentsOfPhoto[pos].Count * 5];
            for (int i = 0; i < commentsOfPhoto[pos].Count; i++)
            {
                marks[i] = -1;
                string index = "";
                if (!Program.showLabel)
                    index = (i + 1) + ". ";
                commentLabels[i] = new System.Windows.Forms.Label();
                commentLabels[i].AutoSize = true;
                commentLabels[i].Size = new System.Drawing.Size(45, 16);
                commentLabels[i].Font = new System.Drawing.Font("Microsoft Sans Serif", 12.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
                commentLabels[i].Text = index + commentsOfPhoto[pos][i];
                commentLabels[i].Width = (int)(rightLayout.Width - 10);
                commentLabels[i].MaximumSize = new Size((int)(rightLayout.Width - 40), 0);
                flows[i] = new FlowLayoutPanel();
                flows[i].MinimumSize = new Size(0, 30);
                flows[i].Size = new System.Drawing.Size(rightLayout.Width - 40, 50);
                if (Program.showLabel)
                {
                    for (int j = 0; j < 5; j++)
                    {
                        int idx = i * 5 + j;
                        points[idx] = new RadioButton();
                        points[idx].AutoSize = true;
                        points[idx].Size = new System.Drawing.Size(64, 17);
                        points[idx].Name = "radioButton" + idx;
                        points[idx].Text = j + "           ";
                        points[idx].Checked = false;
                        flows[i].Controls.Add(points[idx]);
                    }
                }
            }
            for (int i = 0; i < commentsOfPhoto[pos].Count; i++)
            {
                flows[i].Width = rightLayout.Width - 5;
                rightLayout.Controls.Add(commentLabels[i]);
                rightLayout.Controls.Add(flows[i]);
            }
            rightLayout.Controls.Add(NextBtn);
            rightLayout.Controls.Add(PreviousBtn);

            if (Program.showLabel)
            {
                foreach (var point in points)
                    point.CheckedChanged += radioBtn_CheckedChange;
            }

            photo.ImageLocation = photoNames[pos];

            if (commentsOfPhoto[pos].Count > 0)
                NextBtn.Enabled = false;
            if (!Program.showLabel)
                NextBtn.Enabled = true;
        }

        // save the marks of the current photo
        void saveMarks()
        {
            string[] splitName = photoNames[pos].Split('\\');
            StreamWriter sw = new StreamWriter(Program.username + "\\" + splitName[splitName.Length - 1] + "_label.txt");
            for (int i = 0; i < commentsOfPhoto[pos].Count; i++)
            {
                sw.WriteLine(marks[i] + "\t" + commentsOfPhoto[pos][i]);
            }
            sw.Close();
        }

        // finish one label, save the marks of the current photo
        // and then update the form to show next photo
        private void Next_Click(object sender, EventArgs e)
        {
            if (Program.showLabel)
                saveMarks();
            if (pos < photoNames.Length - 1)
            {
                pos += 1;
                updateMsg();
            }
            else
            {
                NextBtn.Visible = false;
                PreviousBtn.Visible = false;
                rightLayout.Visible = false;
                photo.Visible = false;
                label32.Visible = true;
            }
        }

        public void radioBtn_CheckedChange(object sender, EventArgs e)
        {
            string name = (sender as RadioButton).Name;
            int index = int.Parse(name.Substring(11, name.Length - 11)) / labelAmount;
            marks[index] = int.Parse(name.Substring(11, name.Length - 11)) % labelAmount;
            bool finishFlag = true;
            for (int i = 0; i < commentsOfPhoto[pos].Count; i++)
            {
                if (marks[i] == -1)
                {
                    finishFlag = false;
                    break;
                }
            }
            if (finishFlag)
                NextBtn.Enabled = true;
        }

        private void rightLayout_Resize(object sender, EventArgs e)
        {
            for (int i = 0; i < flows.Length; i++)
            {
                flows[i].Width = (int)(rightLayout.Width - 40);
                commentLabels[i].Width = (int)(rightLayout.Width - 40);
                commentLabels[i].MaximumSize = new Size((int)(rightLayout.Width - 40), 0);
            }
        }


        private void LabelForm_Resize(object sender, EventArgs e)
        {
            globalLayout.Width = this.Width - 15;
            globalLayout.Height = this.Height - 50;
            leftLayout.Width = (int)(globalLayout.Width * (4.7 / 9));
            leftLayout.Height = globalLayout.Height - 20;
            photo.Width = (int)(globalLayout.Width * (4.7 / 9));
            photo.Height = globalLayout.Height - 70;
            rightLayout.Width = (int)((globalLayout.Width - 20)* (4.2 / 9)) - 10;
            rightLayout.Height = globalLayout.Height - 50;
            this.MinimumSize = new Size(0, this.Height);
        }

        private void button1_Click(object sender, EventArgs e)
        {
            //if (Program.showLabel)
            //    saveMarks();
            if (pos > 0)
            {
                pos -= 1;
                updateMsg();
            }
            else
            {
                //do nothing
            }
        }

        private void rightLayout_Paint(object sender, PaintEventArgs e)
        {

        }

    }
}
