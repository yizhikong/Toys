using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.IO;

namespace splitWord
{
    public partial class CSpliter : Form
    {
        private CAlphaTree tree;
        private string m_insertTip = "插入{0}成功\n字典树里共有{1}个单词";
        private string m_loadTip = "加载成功\n字典树里共有{0}个单词";
        private string m_notExistTip = "字典树中不存在此单词";
        private string m_existTip = "字典树中存在{0}\n" +
            "以此单词为前缀的单词有{1}个";

        public CSpliter()
        {
            InitializeComponent();
            tree = new CAlphaTree();
        }

        private void btn_insert_Click(object sender, EventArgs e)
        {
            string word = tx_insert.Text.ToString();

            tree.insertWord(word);
            tx_answer.Text = string.Format(m_insertTip, word, tree.Count);
            tx_insert.Text = "";
        }

        private void btn_split_Click(object sender, EventArgs e)
        {
            DateTime begin = DateTime.UtcNow;
            string feedback = tree.splitSentence(tx_sentence.Text.ToString());
            string costTime = (DateTime.UtcNow - begin).ToString();

            tx_answer.Text = feedback + "\ncost time : " + costTime;
            tx_search.Text = "";
        }

        private void btn_search_Click(object sender, EventArgs e)
        {
            string word = tx_search.Text.ToString();
            int time = tree.searchWord(word);

            if (time == 0)
            {
                tx_answer.Text = m_notExistTip;
            }
            else
            {
                tx_answer.Text = string.Format(m_existTip, word, time);
            }

            tx_search.Text = "";
        }

        private void btn_load_Click(object sender, EventArgs e)
        {
            tree = CAlphaTree.createTreeByFile("H://code//splitWord//sentences.txt");
            tx_answer.Text = string.Format(m_loadTip, tree.Count);
        }
    }

    public class CNode
    {
        private CNode[] m_child;
        public bool fWord { set; get; }
        public int iTime { set; get; }

        public CNode()
        {
            m_child = null;
            fWord = false;
            iTime = 0;
        }

        public static int getIndex(char ch)
        {
            int idx = Char.IsDigit(ch) ? ch - '0' + 26 : ch - 'a';

            return idx;
        }

        public CNode this[int idx]
        {
            set
            {
                if (m_child == null)
                {
                    // how many character? 26 + 10 or 26
                    m_child = new CNode[26 + 10];
                }

                m_child[idx] = value;
            }

            get
            {
                if (m_child == null)
                {
                    return null;
                }
                else
                {
                    return m_child[idx];
                }
            }
        }
    }

    public class CAlphaTree
    {
        private CNode m_root;
        private int m_depth;
        private List<List<string>> answers;
        public int Count { set; get; }

        public CAlphaTree()
        {
            m_root = new CNode();
            Count = 0;
            m_depth = 0;
        }

        /*****************************************************************************\
        Function Description:
        
        Create a alpha tree by the contain in a file. The contain in file will be split
        to words. Single quote mark will be replaced with " i". For example
            that's   will be replace as   that is
        
        Arguments:

          [IN] filename - the full path of file, which contains words
        
        Return Value:
        
          return-value - an alpha tree
        
        History:
        
          Created on 08/dd/2015 by jiaweichen_yzkk

        \*****************************************************************************/

        public static CAlphaTree createTreeByFile(string filename)
        {
            if (filename == "" || filename == null)
            {
                return null;
            }

            CAlphaTree tree = new CAlphaTree();
            StreamReader reader = new StreamReader(filename);
            string txt = reader.ReadToEnd();
            char[] spiltChars = {' ', ',', '\n', '\t', '-', '"', '(', ')',
                                    '\'', '.', '\r', '[', ']'};
            string[] words = txt.Replace("'s", " is").Split(spiltChars);

            foreach (string word in words)
            {
                if (word.Length == 0)
                {
                    continue;
                }

                try
                {
                    tree.insertWord(word.ToLower());
                }
                catch (IndexOutOfRangeException e)
                {
                    Console.WriteLine(word);
                }
            }
            return tree;
        }

        public void insertWord(string word)
        {
            // outside word will change?
            word = word.ToLower();

            if (word.Length > m_depth)
            {
                m_depth = word.Length;
            }

            CNode currentNode = m_root;
            int i;

            for (i = 0; i < word.Length; ++i)
            {
                int idx = CNode.getIndex(word[i]);

                if (currentNode[idx] == null)
                {
                    currentNode[idx] = new CNode();
                }
                // add prefix
                currentNode[idx].iTime += 1;
                currentNode = currentNode[idx];
            }

            // mark that it is a word
            currentNode.fWord = true;
            // add count
            Count += 1;
        }

        public int searchWord(string word)
        {
            // outside word will change?
            word = word.ToLower();

            CNode currentNode = m_root;
            int i;

            for (i = 0; i < word.Length; ++i)
            {
                int idx = CNode.getIndex(word[i]);

                if (currentNode[idx] == null)
                {
                    return 0;
                }
                currentNode = currentNode[idx];
            }

            if (currentNode.fWord == true)
            {
                return currentNode.iTime;
            }
            else
            {
                return 0;
            }
        }

        /*****************************************************************************\
        Function Description:

        Split a sentence(without space) to severval words according
        the words in alpha tree

        Arguments:

          [IN] sentence - the sentence without space(should only contain alpha/number)

        Return Value:

          return-value - a string which joins the words by space

        History:

          Created on 08/dd/2015 by jiaweichen_yzkk

        \*****************************************************************************/

        public string splitSentence(string sentence)
        {
            answers = new List<List<string>>();
            List<string> words = new List<string>();

            cutWord(words, sentence.ToLower());
            // cutLongestWord(words, sentence.ToLower());

            StringBuilder result = new StringBuilder();

            foreach (List<string> answer in answers)
            {
                foreach (string word in answer)
                {
                    result.Append(word + " ");
                }
                result.Append("\n");
            }
            answers = null;
            return result.ToString();
        }

        /*****************************************************************************\
        Function Description:

        cut the longest word in the head of sentence. Using recursion.
        There is a bug(will not succeed when the longest word is not the correct word)

        Arguments:

          [IN] words - the list contain the words which were cut away from the sentence before
          [IN] sentence - the uncut sentence without space(should only contain alpha/number)

        Return Value:

          NONE

        History:

          Created on 08/dd/2015 by jiaweichen_yzkk

        \*****************************************************************************/

        private void cutLongestWord(List<string> words, string sentence)
        {
            int i = 0;

            while (true)
            {
                int length = (sentence.Length - i < m_depth) ?
                    sentence.Length - i : m_depth;

                if (length == 0)
                {
                    break;
                }

                string fragment = sentence.Substring(i, length);
                string maxMatchStr = getMaxMatch(fragment);

                words.Add(maxMatchStr);
                i += maxMatchStr.Length;
            }
            answers.Add(words);
        }

        private string getMaxMatch(string fragment)
        {
            List<string> words = new List<string>();
            CNode currentNode = m_root;
            int i;

            for (i = 0; i < fragment.Length; ++i)
            {
                int idx = CNode.getIndex(fragment[i]);

                if (currentNode[idx] == null)
                {
                    break;
                }
                currentNode = currentNode[idx];
                if (currentNode.fWord == true)
                {
                    words.Add(fragment.Substring(0, i + 1));
                }
            }
            return words[words.Count - 1];
        }


        /*****************************************************************************\
        Function Description:
        
        cut the words in the head of sentence. Each possible word will be test(recursion)
        
        Arguments:
        
          [IN] words - the list contain the words which were cut away from the sentence before
          [IN] sentence - the uncut sentence without space(should only contain alpha/number)
        
        Return Value:
        
          NONE
        
        History:
        
          Created on 08/dd/2015 by jiaweichen_yzkk
        
        \*****************************************************************************/

        private void cutWord(List<string> words, string sentence)
        {
            CNode currentNode = m_root;
            int i;

            for (i = 0; i < sentence.Length; ++i)
            {
                int idx = CNode.getIndex(sentence[i]);

                if (currentNode[idx] == null)
                {
                    return;
                }
                currentNode = currentNode[idx];
                if (currentNode.fWord == true)
                {
                    List<string> tryWords = new List<string>();

                    foreach (string word in words)
                    {
                        tryWords.Add(word);
                    }
                    tryWords.Add(sentence.Substring(0, i + 1));
                    // the last word is also a word, parse to a sentence
                    if (i == sentence.Length - 1)
                    {
                        answers.Add(tryWords);
                        return;
                    }
                    string nextStr = sentence.Substring(i + 1,
                        sentence.Length - i - 1);

                    cutWord(tryWords, nextStr);
                }
            }
        }
    }
}
