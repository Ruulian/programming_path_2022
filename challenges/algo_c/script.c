#include <stdio.h>

int main()
{
    char last[22] = "ek`fzm/s^2`rX^/tsoTs|";
    char flag[22] = {};
    for(int i = 0; i < 22; i++){
        if(last[i] != '\0'){
            flag[i] = last[i] + 1;
        }
        else{
            flag[i] = last[i];
        }
    }
    printf("%s\n", flag);
    return 0;
}
