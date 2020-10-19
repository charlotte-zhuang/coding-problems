# What Does It Mean? (trie)
[What Does It Mean?](https://open.kattis.com/problems/heritage)

We can use a _trie_ to store our dictionary of words and the number of meaning each word corresponds to. This allows us to iterate through a name character by character and keep track of all the different word-paths we can take to reach that character.

A [Trie](https://www.geeksforgeeks.org/trie-insert-and-search/) is a tree where the children represent the next element (character) of a pattern (word). When a pattern is finished, the node is marked as an end-node. Patterns are represented as paths of nodes from the root to an end-node.

> Example (slightly different from the sample input)  
> Dictionary: `hei, mark, heim, ark, mei`  
> end-nodes are marked with `/ /`  
```ruby
        =>  a   =>  r   =>  /k/

root    =>  h   =>  e   =>  /i/ =>  /m/

        =>  m   =>  a   =>   r  =>  /k/
                =>  e   =>  /i/
```

Since the input size for the problem is not too big, we can afford to be inefficient in how we keep track of our multiple paths—my pseudocode uses a hash table. Dynamic programming can be used to make runtime linear to the length of the name; see [Aho-Corasick Algorithm for Pattern Searching](https://www.geeksforgeeks.org/aho-corasick-algorithm-pattern-searching/) for details.
- - - -
## Node Class
Nodes only need to store a few instance fields.
The children are stored in an array the size of the alphabet, one index for each character. If the child does not exist, it will be null.
```
child_nodes[]
is_word
num_meanings
```
- - - -
## Trie Class
Store the root in `root_node`

### Insert Function
Add a word to this trie by starting from the root and pathing down to the appropriate child. If child was not initialized, that means this word is the first to go down this path.

Words will share paths if they start with the same characters, then branch out once there’s a difference. If a duplicate word is inserted, only the number of meanings from the second word is kept (since they would have identical paths and end-nodes).

Note that an end-node is not a leaf and can have children. When that happens, it means that a word is fully contained by another word.
> For example, consider ’ten’ and ‘tennis  
> end-nodes are underlined  
> root -> t -> e -> _n_ -> n -> i -> _s_  

```ruby
word
num_meanings
curr_node = root_node

for each c in word
    if (curr_node.child_nodes[c] != nil)
        curr_node.child_nodes[c] = new Node
    curr_node = curr_node.child_nodes[c]

# curr_node is now the last node for word
curr_node.is_end = true
curr_node.num_meanings = num_meanings
```

### Search Function
Use a table to keep track of nodes that reached a character and the cumulative number of paths the node represents.
1. Start from the root with 0 meanings
2. Iterate through each character in the name
3. Check the nodes from your table and add to the next character’s table
    1. Add their children if they exist
    2. Also add the root if the child is an end-node
        * This means that it’s possible to start a new word
        * Multiply the path’s number of meanings by the child’s number of meanings when adding to the root
4. Return the number of meanings at the root
    * This represents the number of paths that end at the end of the name
```ruby
name        # name we are searching for
nodes_table # key = node; value = meanings for that node

# start with a new word, 0 meanings    
nodes_table.add(root_node, 0)
for each c in name
    next_table # nodes_table for next c
    # add to next_table if c can be reached
    for each node in nodes_table
        child_node = node.child_nodes[c]
        Path_Into child_node
    nodes_table = next_table

# return the number of meanings that ended
return nodes_table.contains(root_node) ?
    nodes_table.get(root_node) : 0
```

### Path Into a node
```ruby
child_node  # node to path into
next_table  # add path here

if (child_node != nil)  # node is a valid path
    next_table.add(child_node, nodes_table.get(node))

    if (child_node.is_end)  # use child as a word
        # do not multiply by zero
        path_meanings = nodes_table.get(node) != 0 ?
            nodes_table.get(node) : 1
        # multiply values by num_meanings and add to root
        path_meanings *= child_node.num_meanings
        path_meanings += next_table.get(root_node)
        path_meanings % 1,000,000,007   # prevent overflow
        next_table.set(root_node, path_meanings)
```
- - - -
## Example
Dictionary: `hei 2, mark 2, heim 1, ark 2, heima 1`
Name: `heimark`
### Constructing the Trie
end-nodes are marked with their number of meanings
```ruby
        =>  a   =>  r   =>  k:2
root    =>  h   =>  e   =>  i:2 =>  m:1 => a:1
        =>  m   =>  a   =>  r   =>  k:2
```
### Searching
0. **start**

_table_
`root`: `0`

1. **h**

_table_
`root` -> `h: 0`

2. **e**

_table_
`h` -> `e: 0`

3. **i**

_table_
`he` -> `root: 2`
`he` -> `i: 0`
_Explanation_
    1. Use the word `hei` with 2 meanings, returning to the root to start a new word.
    2. Continue from `he` -> `i` and carry 0 meanings forwards.

4. **m**

_table_
`root` -> `m: 2`
`hei` -> `root: 1`
`hei` -> `m: 0`
_Explanation_
    1. `root` -> `m`: carry 2 meanings forwards
    2. `hei` -> `root`: use the word `heim` with 1 meaning
    3. `hei` -> `m`: carry 0 meanings forwards

5. **a**

_table_
`m` -> `a: 2`
`root` -> `a: 1`
`heim` -> `root: 1`
`heim` -> `a: 0`
_Explanation_
    1. `m` -> `a`: carry 2 meanings forwards
    2. `root` -> `a`: carry 1 meaning forwards
    3. `heim` -> `root`: use the word `heima` with 1 meaning
    4. `heim` -> `a`: carry 0 meanings forwards
    
_Note_: we still add the path `heima` to the table even though there’s nowhere for it to go. Since we aren’t checking if `a` is a leaf, there may be more children to traverse.

6. **r**

_table_
`ma` -> `r: 2`
`a` -> `r: 1`
`root` -> `nil`
`heima` -> `nil`
_Explanation_
    1. `ma` -> `r`: carry 2 meanings forwards
    2. `a` -> `r`: carry 1 meaning forwards
    3. `root` -> does not have child `r`
    4. `heima` -> does not have child `r`

7. **k**

_table_
`mar` -> `root: 4`  _2 · 2 = 4_
`mar` -> `k: 2`
`ar` -> `root: 6`  _4 + 1 · 2 = 6 replaces previous root entry_
`ar` -> `k: 1`
_Explanation_
    1. `mar` -> `root`:
        1. use the word `mark` with 2 meanings
        2. multiply by path’s carried 2 meanings
        3. store 4 in root
    2. `mar` -> `k`: carry 2 meanings forwards
    3. `ar` -> `root`: 
        1. use the word `ark` with 2 meanings
        2. multiply by path’s carried 1 meaning
        3. add 2 to root
    4. `ar` -> `k`: carry 1 meaning forwards
    
8. **return 6**

_Explanation_
We’ve reached the end of the name and return the value stored in root. The paths `mark` and `ark` still in our table cannot be used because they did not terminate at the end of the name.

_by charlotte_