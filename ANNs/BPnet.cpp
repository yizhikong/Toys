#include <iostream>
#include <cstdio>
#include <cstdlib>
#include <vector>
#include <ctime>
#include <cmath>
#define dVector std::vector<std::vector<double> >
#define Net std::vector<std::vector<Sigmoid> >
class Sigmoid {
public:
    Sigmoid(int n_, int eta_) : n(n_) {
        srand(unsigned(time(0)));
        int i;
        // n inputs plus x0(1)
        // initial in range -0.05 ~ 0.05
        for (i = 0; i < n; i++)
            weight.push_back(double(rand() % 100) / 1000 - 0.05);
    }
    double output(std::vector<double> example) {
        double o = 0;
        int i;
        for (i = 0; i < n; i++)
            o += example[i] * weight[i];
        double sigma = 1.0 / (1 + exp(-o));
        return sigma;
    }
    std::vector<double> weight;
private:
    // the number of inputs
    int n;
};

dVector tests;

double net_test(Net net, int n_in, int n_out, int n_hidden) {
    int right = 0;
    int all = tests.size();
    int t;
    for (t = 0; t < all; t++) {
        std::vector<double> outputOfHidden;
        int h;
        for (h = 0; h < n_hidden; h++)
            outputOfHidden.push_back(net[0][h].output(tests[t]));
        std::vector<double> finalOutput;
        int o;
        for (o = 0; o < n_out; o++)
            finalOutput.push_back(net[1][o].output(outputOfHidden));
        int pos = 0;
        double max = finalOutput[0];
        for (o = 1; o < n_out; o++)
            if (finalOutput[o] > max) {
                max = finalOutput[o];
                pos = o;
            }
        //printf("output %d vs %d with %lf\n", pos, tests[t][n_in], max);
        if (pos == tests[t][n_in]) {
            //printf("output %d the same as %d with %lf\n", pos, tests[t][n_in], max);
            right++;
        }
    }
    // printf("total %d test, hit %d\n", all, right);
    return double(right) / (all);
}

Net BACKPROPAGATION(dVector examples, double eta, int n_in, int n_out, int n_hidden) {
    // create the artificial neural network
    std::vector<Sigmoid> hidden;
    std::vector<Sigmoid> out;
    int i;
    // n_hidden Sigmoid unit(with n_in inputs)
    for (i = 0; i < n_hidden; i++) {
        Sigmoid temp(n_in, eta);
        hidden.push_back(temp);
    }
    // n_out Sigmoid unit(with n_hidden inputs)
    // 0100000000 means 1, 0010000000 means 2
    for (i = 0; i < n_out; i++) {
        Sigmoid temp(n_hidden, eta);
        out.push_back(temp);
    }
    // the number of example
    int t = examples.size();
    int step = 0;
    int MAX_STEP = 200;
    int END_FLAG = 0;
    while(END_FLAG ==0 && step < MAX_STEP) {
        printf("in %dth run\n", step++);
        int e;
        // for every exmaple
        // for every exmaple
        double checkDelta = 0;
        for (e = 0; e < t; e++) {
            // express the target number as 0010000000
            std::vector<double> target;
            int t;
            for (t = 0; t < n_out; t++)
                target.push_back(0);
            // set the target pos to 1
            int targetPos = examples[e][n_in];
            target[targetPos] = 1;
            // forward propagation
            std::vector<double> outputOfHidden;
            int h;
            for (h = 0; h < n_hidden; h++)
                outputOfHidden.push_back(hidden[h].output(examples[e]));
            std::vector<double> finalOutput;
            int o;
            // the outputOfHidden is the input of output layer
            for (o = 0; o < n_out; o++)
                finalOutput.push_back(out[o].output(outputOfHidden));
            // backward propagation
            // count the delta of output unit
            std::vector<double> deltaOfOutput;
            for (o = 0; o < n_out; o++) {
                double temp = finalOutput[o];
                deltaOfOutput.push_back(temp * (1 - temp) * (target[o] - temp));
                double del = target[o] - finalOutput[o];
                checkDelta += del * del;
            }
            // count the delta of hidden unit
            std::vector<double> deltaOfHidden;
            for (h = 0; h < n_hidden; h++) {
                double temp = outputOfHidden[h];
                double sum = 0;
                for (o = 0; o < n_out; o++)
                    sum += out[o].weight[h] * deltaOfOutput[o];
                deltaOfHidden.push_back(temp * (1 - temp) * sum);
            }
            // update the weight of hidden unit
            for (h = 0; h < n_hidden; h++) {
                for (i = 0; i < n_in; i++)
                    hidden[h].weight[i] += eta * deltaOfHidden[h] * examples[e][i];
            }
            // update the weight of output unit
            for (o = 0; o < n_out; o++) {
                for (h = 0; h < n_hidden; h++)
                    out[o].weight[h] += eta * deltaOfOutput[o] * outputOfHidden[h];
            }
        }
        Net currentNet;
        currentNet.push_back(hidden);
        currentNet.push_back(out);
        double correctRate = net_test(currentNet, n_in, n_out, n_hidden);
        checkDelta /= 2;
        printf("             ==> current delta of is %lf\n", checkDelta / t);
        printf("             ==> current accuracy %lf\n", correctRate);
        if (checkDelta / t < 0.02)
            END_FLAG = 1;
    }
    Net net;
    net.push_back(hidden);
    net.push_back(out);
    return net;
}
int main(int argc, char* argv[]) {
    if (argc > 1) {
        freopen(argv[1], "r", stdin);
    } else {
        printf("please run the program as \"BPnet.exe [tranning_file_name] [testing_file_name]\"\n");
        exit(0);
    }
    dVector examples;
    while(1) {
        int eof = 0;
        std::vector<double> example;
        int i;
        for (i = 0; i < 65; i++) {
            double temp;
            if (scanf("%lf", &temp) != EOF) {
                getchar();
                if (i != 64)
                    temp /= 16;
                example.push_back(temp);
            } else {
                eof = 1;
                break;
            }
        }
        if (eof == 1)
            break;
        //printf("%d\n", example[65]);
        examples.push_back(example);
    }
    if (argc > 2) {
        fflush(stdin);
        freopen(argv[2], "r", stdin);
        while(1) {
            int eof = 0;
            std::vector<double> test;
            int i;
            for (i = 0; i < 65; i++) {
                double temp;
                if (scanf("%lf", &temp) != EOF) {
                    getchar();
                    if (i != 64)
                        temp / 16;
                    test.push_back(temp);
                } else {
                    eof = 1;
                    break;
                }
            }
            if (eof == 1)
                break;
            tests.push_back(test);
        }
    }
    printf("train begin with %d traning data\n", examples.size());
    Net ans = BACKPROPAGATION(examples, 0.25, 64, 10, 32);
    printf("\nTrain over, the accuracy is %lf\n", net_test(ans, 64, 10, 32));
    return 0;
}
