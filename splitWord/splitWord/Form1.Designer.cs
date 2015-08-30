namespace splitWord
{
    partial class CSpliter
    {
        /// <summary>
        /// 必需的设计器变量。
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// 清理所有正在使用的资源。
        /// </summary>
        /// <param name="disposing">如果应释放托管资源，为 true；否则为 false。</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows 窗体设计器生成的代码

        /// <summary>
        /// 设计器支持所需的方法 - 不要
        /// 使用代码编辑器修改此方法的内容。
        /// </summary>
        private void InitializeComponent()
        {
            this.tx_insert = new System.Windows.Forms.TextBox();
            this.tx_sentence = new System.Windows.Forms.TextBox();
            this.btn_insert = new System.Windows.Forms.Button();
            this.btn_split = new System.Windows.Forms.Button();
            this.tx_answer = new System.Windows.Forms.Label();
            this.tx_label = new System.Windows.Forms.Label();
            this.tx_search = new System.Windows.Forms.TextBox();
            this.btn_search = new System.Windows.Forms.Button();
            this.btn_load = new System.Windows.Forms.Button();
            this.SuspendLayout();
            // 
            // tx_insert
            // 
            this.tx_insert.Location = new System.Drawing.Point(28, 44);
            this.tx_insert.Name = "tx_insert";
            this.tx_insert.Size = new System.Drawing.Size(126, 21);
            this.tx_insert.TabIndex = 0;
            // 
            // tx_sentence
            // 
            this.tx_sentence.Location = new System.Drawing.Point(28, 107);
            this.tx_sentence.Name = "tx_sentence";
            this.tx_sentence.Size = new System.Drawing.Size(126, 21);
            this.tx_sentence.TabIndex = 1;
            // 
            // btn_insert
            // 
            this.btn_insert.Location = new System.Drawing.Point(170, 41);
            this.btn_insert.Name = "btn_insert";
            this.btn_insert.Size = new System.Drawing.Size(75, 23);
            this.btn_insert.TabIndex = 2;
            this.btn_insert.Text = "添加词汇";
            this.btn_insert.UseVisualStyleBackColor = true;
            this.btn_insert.Click += new System.EventHandler(this.btn_insert_Click);
            // 
            // btn_split
            // 
            this.btn_split.Location = new System.Drawing.Point(170, 107);
            this.btn_split.Name = "btn_split";
            this.btn_split.Size = new System.Drawing.Size(75, 23);
            this.btn_split.TabIndex = 3;
            this.btn_split.Text = "进行分词";
            this.btn_split.UseVisualStyleBackColor = true;
            this.btn_split.Click += new System.EventHandler(this.btn_split_Click);
            // 
            // tx_answer
            // 
            this.tx_answer.AutoSize = true;
            this.tx_answer.Location = new System.Drawing.Point(26, 180);
            this.tx_answer.Name = "tx_answer";
            this.tx_answer.Size = new System.Drawing.Size(0, 12);
            this.tx_answer.TabIndex = 4;
            // 
            // tx_label
            // 
            this.tx_label.AutoSize = true;
            this.tx_label.Location = new System.Drawing.Point(28, 157);
            this.tx_label.Name = "tx_label";
            this.tx_label.Size = new System.Drawing.Size(29, 12);
            this.tx_label.TabIndex = 5;
            this.tx_label.Text = "结果";
            // 
            // tx_search
            // 
            this.tx_search.Location = new System.Drawing.Point(28, 75);
            this.tx_search.Name = "tx_search";
            this.tx_search.Size = new System.Drawing.Size(126, 21);
            this.tx_search.TabIndex = 6;
            // 
            // btn_search
            // 
            this.btn_search.Location = new System.Drawing.Point(170, 75);
            this.btn_search.Name = "btn_search";
            this.btn_search.Size = new System.Drawing.Size(75, 23);
            this.btn_search.TabIndex = 7;
            this.btn_search.Text = "搜索词汇";
            this.btn_search.UseVisualStyleBackColor = true;
            this.btn_search.Click += new System.EventHandler(this.btn_search_Click);
            // 
            // btn_load
            // 
            this.btn_load.Location = new System.Drawing.Point(28, 11);
            this.btn_load.Name = "btn_load";
            this.btn_load.Size = new System.Drawing.Size(217, 23);
            this.btn_load.TabIndex = 8;
            this.btn_load.Text = "从文件中加载词汇";
            this.btn_load.UseVisualStyleBackColor = true;
            this.btn_load.Click += new System.EventHandler(this.btn_load_Click);
            // 
            // CSpliter
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 12F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(270, 345);
            this.Controls.Add(this.btn_load);
            this.Controls.Add(this.btn_search);
            this.Controls.Add(this.tx_search);
            this.Controls.Add(this.tx_label);
            this.Controls.Add(this.tx_answer);
            this.Controls.Add(this.btn_split);
            this.Controls.Add(this.btn_insert);
            this.Controls.Add(this.tx_sentence);
            this.Controls.Add(this.tx_insert);
            this.Name = "CSpliter";
            this.Text = "CSpliter";
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.TextBox tx_insert;
        private System.Windows.Forms.TextBox tx_sentence;
        private System.Windows.Forms.Button btn_insert;
        private System.Windows.Forms.Button btn_split;
        private System.Windows.Forms.Label tx_answer;
        private System.Windows.Forms.Label tx_label;
        private System.Windows.Forms.TextBox tx_search;
        private System.Windows.Forms.Button btn_search;
        private System.Windows.Forms.Button btn_load;
    }
}

