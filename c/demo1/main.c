// mian.c

#include <stdio.h>

#include <stdio.h>  
#include <string.h> 
#include <stdlib.h> 

#define MAX 7  // 哈希表的大小（桶的数量）
typedef int datatype_t;  // 定义数据类型为int

// 哈希表节点结构（用于链表）
typedef struct node {
    datatype_t data;       // 存储的数据
    struct node* next;     // 指向下一个节点的指针，用于处理哈希冲突
}hashtable_t;

/**
 * 创建哈希表
 * 返回值：指向哈希表（指针数组）的指针
 */
hashtable_t** create_hashtable()
{
    int i = 0;
    hashtable_t** h = NULL;  // 哈希表指针（指向指针数组的指针）

    // 为哈希表分配内存，大小为MAX个hashtable_t*类型的指针
    h = (hashtable_t**)malloc(MAX * sizeof(hashtable_t*));
    // 将哈希表所有元素初始化为0（NULL）
    // 注意：原代码此处有小问题，正确应为memset(h, 0, MAX * sizeof(hashtable_t *));
    memset(h, 0, sizeof(MAX * sizeof(hashtable_t*)));

    // 再次确保每个桶的头指针都为NULL（双重保险）
    for (i = 0; i < MAX; i++)
    {
        h[i] = NULL;
    }
    return h;  // 返回创建好的哈希表
}

/**
 * 向哈希表中插入数据
 * @param h 哈希表指针
 * @param key 要插入的数据
 */
void insert_data_hash(hashtable_t** h, datatype_t key)
{
    hashtable_t* temp = NULL;  // 新节点指针
    hashtable_t** p = NULL;    // 用于遍历链表的二级指针

    int index = 0;
    // 计算哈希索引：使用取模运算得到0~MAX-1的索引值
    index = key % MAX;

    /* 遍历对应索引的链表，找到插入位置
     保持链表按数据大小升序排列，提高查找效率
    二级指针p的地址一直没有变，变得只是二级指针里存的一级指针，
    二级指针p表示输出的是一级指针，*p表示一级指针h[index]输出的地址。*/
    for (p = &h[index]; *p != NULL; p = &((*p)->next))
    {
        // 当找到第一个大于key的节点时，停止遍历（插入到该节点前）
        if ((*p)->data > key)
            break;
    }

    // 创建新节点
    temp = (hashtable_t*)malloc(sizeof(hashtable_t));
    temp->data = key;         // 存储数据
    temp->next = *p;          // 新节点指向当前节点
    *p = temp;                // 当前位置指向新节点，完成插入
    return;
}


/**
 * 打印哈希表中的所有数据
 * @param h 哈希表指针
 */
void printf_hash_table(hashtable_t** h)
{
    int i = 0;
    hashtable_t** p = NULL;   // 用于遍历链表的二级指针

    // 遍历哈希表的每个索引（每个桶）
    for (i = 0; i < MAX; i++)
    {
        printf("index = %d : ", i);  // 打印当前索引

        // 遍历当前索引对应的链表并打印所有数据
        for (p = &h[i]; *p != NULL; p = &((*p)->next))
        {
            printf("%d ", (*p)->data);
        

int testFunc() {
	// 随便写点逻辑验证
	return 0;
}

int main() {
	printf("程序启动...\n");

	testFunc();
	return 0;
}