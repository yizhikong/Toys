namespace Label
{
    partial class LabelForm
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.photo = new System.Windows.Forms.PictureBox();
            this.rightLayout = new System.Windows.Forms.FlowLayoutPanel();
            this.percent_label = new System.Windows.Forms.Label();
            this.label32 = new System.Windows.Forms.Label();
            this.globalLayout = new System.Windows.Forms.FlowLayoutPanel();
            this.leftLayout = new System.Windows.Forms.FlowLayoutPanel();
            ((System.ComponentModel.ISupportInitialize)(this.photo)).BeginInit();
            this.globalLayout.SuspendLayout();
            this.leftLayout.SuspendLayout();
            this.SuspendLayout();
            // 
            // photo
            // 
            this.photo.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom) 
            | System.Windows.Forms.AnchorStyles.Left)));
            this.photo.BackColor = System.Drawing.SystemColors.ActiveCaptionText;
            this.photo.Location = new System.Drawing.Point(3, 19);
            this.photo.Name = "photo";
            this.photo.Size = new System.Drawing.Size(700, 669);
            this.photo.SizeMode = System.Windows.Forms.PictureBoxSizeMode.Zoom;
            this.photo.TabIndex = 0;
            this.photo.TabStop = false;
            // 
            // rightLayout
            // 
            this.rightLayout.AutoScroll = true;
            this.rightLayout.BackColor = System.Drawing.SystemColors.Control;
            this.rightLayout.FlowDirection = System.Windows.Forms.FlowDirection.TopDown;
            this.rightLayout.Location = new System.Drawing.Point(719, 3);
            this.rightLayout.MinimumSize = new System.Drawing.Size(60, 0);
            this.rightLayout.Name = "rightLayout";
            this.rightLayout.Padding = new System.Windows.Forms.Padding(10, 15, 0, 30);
            this.rightLayout.Size = new System.Drawing.Size(449, 697);
            this.rightLayout.TabIndex = 3;
            this.rightLayout.WrapContents = false;
            this.rightLayout.Paint += new System.Windows.Forms.PaintEventHandler(this.rightLayout_Paint);
            this.rightLayout.Resize += new System.EventHandler(this.rightLayout_Resize);
            // 
            // percent_label
            // 
            this.percent_label.AutoSize = true;
            this.percent_label.Font = new System.Drawing.Font("Microsoft Sans Serif", 9.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.percent_label.Location = new System.Drawing.Point(3, 0);
            this.percent_label.Name = "percent_label";
            this.percent_label.Size = new System.Drawing.Size(52, 16);
            this.percent_label.TabIndex = 4;
            this.percent_label.Text = "label31";
            // 
            // label32
            // 
            this.label32.AutoSize = true;
            this.label32.Font = new System.Drawing.Font("Microsoft Sans Serif", 27.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label32.Location = new System.Drawing.Point(560, 314);
            this.label32.Name = "label32";
            this.label32.Size = new System.Drawing.Size(142, 42);
            this.label32.TabIndex = 5;
            this.label32.Text = "Thanks";
            // 
            // globalLayout
            // 
            this.globalLayout.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom) 
            | System.Windows.Forms.AnchorStyles.Left)));
            this.globalLayout.Controls.Add(this.leftLayout);
            this.globalLayout.Controls.Add(this.rightLayout);
            this.globalLayout.Location = new System.Drawing.Point(12, 30);
            this.globalLayout.Name = "globalLayout";
            this.globalLayout.Size = new System.Drawing.Size(1192, 700);
            this.globalLayout.TabIndex = 6;
            // 
            // leftLayout
            // 
            this.leftLayout.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.leftLayout.Controls.Add(this.percent_label);
            this.leftLayout.Controls.Add(this.photo);
            this.leftLayout.FlowDirection = System.Windows.Forms.FlowDirection.TopDown;
            this.leftLayout.Location = new System.Drawing.Point(3, 3);
            this.leftLayout.Name = "leftLayout";
            this.leftLayout.Size = new System.Drawing.Size(710, 721);
            this.leftLayout.TabIndex = 6;
            // 
            // LabelForm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(1234, 742);
            this.Controls.Add(this.label32);
            this.Controls.Add(this.globalLayout);
            this.MaximizeBox = false;
            this.Name = "LabelForm";
            this.Text = "LabelForm";
            this.Resize += new System.EventHandler(this.LabelForm_Resize);
            ((System.ComponentModel.ISupportInitialize)(this.photo)).EndInit();
            this.globalLayout.ResumeLayout(false);
            this.leftLayout.ResumeLayout(false);
            this.leftLayout.PerformLayout();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.PictureBox photo;
        private System.Windows.Forms.FlowLayoutPanel rightLayout;
        private System.Windows.Forms.Label percent_label;
        private System.Windows.Forms.Label label32;
        private System.Windows.Forms.FlowLayoutPanel globalLayout;
        private System.Windows.Forms.FlowLayoutPanel leftLayout;
    }
}

