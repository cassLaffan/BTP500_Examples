#include <iostream>
#include <iomanip>
#include <queue>
#include <cmath>
#include <string>
#include <vector>
#include <random>
#include <algorithm>

template <typename T>
class AVL{
    T data;
    AVL* left = nullptr;
    AVL* right = nullptr;
    int balance = 0;

    // helper functions for breadth first printing
    void printData(T data, int spacing, int balance){
        std::cout << std::setw(spacing) << data << std::setw(3) << balance << std::setw(0);
    }
    void printEmpty(int spacing){
        std::cout << std::setw(spacing) << "_" << std::setw(3) << "_" << std::setw(0);
    }
    void printSpaces(int spacing, int height, bool halfspacing){
        int overallSpacing = (int)(spacing + 3);
        overallSpacing = overallSpacing * 2 * pow(2, height - 2) - (halfspacing?overallSpacing/2:overallSpacing);
        if (overallSpacing > 0)
            std::cout << std::setw(overallSpacing) << " " <<std::setw(0);
    }
public:
    AVL(T data){
        // not allowing invalid data in nodes - could be resolved by using pointers instead. but alas. 
        this->data = data;
    }
    ~AVL(){
        // this program has not been checked for memory leaks
        delete left;
        delete right;
    }
    void rebalancer(){
        if (balance == -2){
            if (left != nullptr and left->balance == 1)
                left->rotateLeft();
            rotateRight();
        }
        else if (balance == 2){
            if (right != nullptr and right->balance == -1)
                right->rotateRight();
            rotateLeft();
        }
    }
    void rotateLeft(){
        if (right == nullptr)
            return;
        AVL* newLeft = new AVL(data);
        // feels like there's a memory leak here somewhere..
        *newLeft = *this; // shallow copy
        newLeft->right = right->left; // copy pointer
        *this = *right; // shallow copy
        left = newLeft; // copy pointer

        if (balance == 1 and left->balance == 2){
            balance = 0;
            left->balance = 0;
        }
        else if (balance == 1 and left->balance == 1){
            balance = -1;
            left->balance = -1;
        }
        else if (balance == 0 and left->balance == 1){
            balance = -1;
            left->balance = 0;
        }
        else if (balance == 0 and left->balance == 2){
            balance = -1;
            left->balance = 1;
        }
        else if (balance == -1 and left->balance == 1){
            balance = -2;
            left->balance = 0;
        }
        else if (balance == 2 and left->balance == 2){
            balance = 0;
            left->balance = -1;
        }
        else{
            std::cout << "AARG";
            throw "a";
        }
    }
    void rotateRight(){
        if (left == nullptr)
            return;
        AVL* newRight = new AVL(data);
        // feels like there's a memory leak here somewhere..
        *newRight = *this; // shallow copy
        newRight->left = left->right; // copy pointer
        *this = *left; // shallow copy
        right = newRight; // copy pointer

        if (balance == -1 and right->balance == -2){
            balance = 0;
            right->balance = 0;
        }
        else if (balance == -1 and right->balance == -1){
            balance = 1;
            right->balance = 1;
        }
        else if (balance == 0 and right->balance == -1){
            balance = 1;
            right->balance = 0;
        }
        else if (balance == 0 and right->balance == -2){
            balance = 1;
            right->balance = -1;
        }
        else if (balance == 1 and right->balance == -1){
            balance = 2;
            right->balance = 0;
        }
        else if (balance == -2 and right->balance == -2){
            balance = 0;
            right->balance = 1;
        }
        else{
            std::cout << "BARG";
            throw "b";
        }
    }
    void insert(T data){
        if (data < this->data){
            if (left != nullptr){
                // used to determine the change in the child's balance
                int oldBalance = left->balance;
                // insert somewhere in the left side
                left->insert(data);
                // recalculate this balance from the bottom up
                if (oldBalance == 0 and abs(left->balance) == 1)
                    balance -= 1;
            }
            else{
                // create sub-AVL tree on the left side
                left = new AVL(data);
                balance -= 1;
            }
        }
        else if (data > this->data){
            if (right != nullptr){
                // used to determine the change in the child's balance
                int oldBalance = right->balance;
                // insert somewhere in the right side
                right->insert(data);
                // recalculate this balance from the bottom up
                if (oldBalance == 0 and abs(right->balance) == 1)
                    balance += 1;
            }
            else{
                // create sub-AVL tree on the right side
                right = new AVL(data);
                balance += 1;
            }
        }
        else
            // data already exists in the AVL tree
            return;

        // rebalance from the bottom up
        if (abs(balance) > 1)
            rebalancer();
    }
    bool search(T data){
        if (this->data == data)
            return true;
        else if (data < this->data && left != nullptr)
            return left->search(data);
        else if (data > this->data && right != nullptr)
            return right->search(data);
        return false;
    }
    int getHeight(){
        return 1 + (balance<0 ? (left?left->getHeight():0) : (right?right->getHeight():0));
    }
    void breadthFirstPrint(int spacing=4){
        int height = getHeight() - 1;
        // rows of the AVL are printed one at a time
        std::queue<AVL*> currentRow = std::queue<AVL*>();
        std::queue<AVL*> nextRow = std::queue<AVL*>();
        // print first row
        printSpaces(spacing, height, true);
        printData(data, spacing, balance);
        currentRow.push(this);
        bool empty = !(left || right); // whether or not any elements were *actually* added to the next row
        while (!empty){
            empty = true;
            std::cout << std::endl;
            height -= 1;
            printSpaces(spacing, height, true);
            height += 1;
            while (!currentRow.empty()){
                AVL* ele = currentRow.front();
                currentRow.pop();
                
                if (ele != nullptr && ele->left != nullptr){
                    // print left child; add left child or nullptr to the next row
                    printData(ele->left->data, spacing, ele->left->balance);
                    nextRow.push(ele->left);
                    if (ele->left->left || ele->left->right)
                        empty = false;
                }
                else{
                    // if this element was nullptr or its child was nullptr, print the placeholder
                    printEmpty(spacing);
                    nextRow.push(nullptr);
                }

                printSpaces(spacing, height, false);

                if (ele != nullptr && ele->right != nullptr){
                    // print right child; add right child or nullptr to the next row
                    printData(ele->right->data, spacing, ele->right->balance);
                    nextRow.push(ele->right);
                    if (ele->right->left || ele->right->right)
                        empty = false;
                }
                else{
                    // if this element was nullptr or its child was nullptr, print the placeholder
                    printEmpty(spacing);
                    nextRow.push(nullptr);
                }

                printSpaces(spacing, height, false);
            }
            height -= 1;
            currentRow = nextRow;
            nextRow = std::queue<AVL*>();
        }
        std::cout << std::endl;
    }
};


int main(){
    int num_elements = 30;

    // create shuffled array from 0 to 29
    std::vector<int> vals = std::vector<int>();
    for (int i = 0; i < num_elements; ++i)
        vals.push_back(i);
    std::random_device rd;
    std::mt19937 g(rd());
    std::shuffle(vals.begin(), vals.end(), g);
    // add first value to AVL (because no-value nodes are not allowed because not using a pointer and not adding a bool)
    AVL avl = AVL(vals[0]);
    // add the other values
    for (int i = 1; i < vals.size(); ++i){
        // avl.breadthFirstPrint();
        std::cout << "inserting " << vals[i] << std::endl;
        avl.insert(vals[i]);
    }
    avl.breadthFirstPrint();
}