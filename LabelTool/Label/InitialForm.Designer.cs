namespace Label
{
    partial class InitialForm
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
            this.select_p_btn = new System.Windows.Forms.Button();
            this.label1 = new System.Windows.Forms.Label();
            this.name_box = new System.Windows.Forms.TextBox();
            this.select_c_btn = new System.Windows.Forms.Button();
            this.showLabelCheckBox = new System.Windows.Forms.CheckBox();
            this.closeBtn = new System.Windows.Forms.Button();
            this.SuspendLayout();
            // 
            // select_p_btn
            // 
            this.select_p_btn.Location = new System.Drawing.Point(157, 225);
            this.select_p_btn.Name = "select_p_btn";
            this.select_p_btn.Size = new System.Drawing.Size(221, 23);
            this.select_p_btn.TabIndex = 0;
            this.select_p_btn.Text = "Select photo path";
            this.select_p_btn.UseVisualStyleBackColor = true;
            this.select_p_btn.Click += new System.EventHandler(this.select_p_btn_Click);
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label1.Location = new System.Drawing.Point(154, 145);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(156, 17);
            this.label1.TabIndex = 1;
            this.label1.Text = "please input your name";
            // 
            // name_box
            // 
            this.name_box.Location = new System.Drawing.Point(157, 165);
            this.name_box.Name = "name_box";
            this.name_box.Size = new System.Drawing.Size(221, 20);
            this.name_box.TabIndex = 2;
            this.name_box.TextChanged += new System.EventHandler(this.name_box_TextChanged);
            // 
            // select_c_btn
            // 
            this.select_c_btn.Location = new System.Drawing.Point(157, 268);
            this.select_c_btn.Name = "select_c_btn";
            this.select_c_btn.Size = new System.Drawing.Size(221, 23);
            this.select_c_btn.TabIndex = 3;
            this.select_c_btn.Text = "Select comment path";
            this.select_c_btn.UseVisualStyleBackColor = true;
            this.select_c_btn.Click += new System.EventHandler(this.select_c_btn_Click);
            // 
            // showLabelCheckBox
            // 
            this.showLabelCheckBox.AutoSize = true;
            this.showLabelCheckBox.Location = new System.Drawing.Point(306, 315);
            this.showLabelCheckBox.Name = "showLabelCheckBox";
            this.showLabelCheckBox.Size = new System.Drawing.Size(72, 17);
            this.showLabelCheckBox.TabIndex = 4;
            this.showLabelCheckBox.Text = "Not Label";
            this.showLabelCheckBox.UseVisualStyleBackColor = true;
            // 
            // closeBtn
            // 
            this.closeBtn.Location = new System.Drawing.Point(303, 352);
            this.closeBtn.Name = "closeBtn";
            this.closeBtn.Size = new System.Drawing.Size(75, 23);
            this.closeBtn.TabIndex = 5;
            this.closeBtn.Text = "Next";
            this.closeBtn.UseVisualStyleBackColor = true;
            this.closeBtn.Click += new System.EventHandler(this.closeBtn_Click);
            // 
            // InitialForm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(582, 523);
            this.Controls.Add(this.closeBtn);
            this.Controls.Add(this.showLabelCheckBox);
            this.Controls.Add(this.select_c_btn);
            this.Controls.Add(this.name_box);
            this.Controls.Add(this.label1);
            this.Controls.Add(this.select_p_btn);
            this.Name = "InitialForm";
            this.Text = "InitialForm";
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Button select_p_btn;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.TextBox name_box;
        private System.Windows.Forms.Button select_c_btn;
        private System.Windows.Forms.CheckBox showLabelCheckBox;
        private System.Windows.Forms.Button closeBtn;
    }
}