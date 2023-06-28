# Prioritised BFS + MaxHeap to find next course of action

class PriorityQueueBase:
# Abstract base class for a priority queue
    class _Node:
        __slots__ = '_vertex' , '_priority'
        def __init__ (self, v, dv):
            self._vertex = v
            self._priority = dv
        
        # OPERATOR OVERLOADING
        def __gt__ (self, other): # compare items based on their priority value
            if (self._priority == 'inf' and other._priority != 'inf'): return True
            if (self._priority != 'inf' and other._priority == 'inf'): return False
            if (self._priority > other._priority): return True
            return False

class HeapPriorityQueue(PriorityQueueBase):
#------------------------------ Non-Public Functions ------------------------------
    def _parent(self, j):
        return (j-1) // 2

    def _left(self, j):
        return 2*j+1

    def _right(self, j):
        return 2*j+2

    def _has_left(self, j):
        return self._left(j) < len(self._data) # index beyond end of list?

    def _has_right(self, j):
        return self._right(j) < len(self._data) # index beyond end of list?

    def _swap(self, i, j):
        # First get all carry forward values of data values at position i and j
        vertexi = self._data[i]._vertex
        vertexj = self._data[j]._vertex

        idw = self._refer[vertexi][1]
        idww = self._refer[vertexi][2]

        jdw = self._refer[vertexj][1]
        jdww = self._refer[vertexj][2]

        self._data[i], self._data[j] = self._data[j], self._data[i]
        self._refer[self._data[i]._vertex]=(i, jdw, jdww)
        self._refer[self._data[j]._vertex]=(j, idw, idww)

    def _upheap(self, j):   # j is the index of the element to be upheaped
        parent = self._parent(j)
        if (j > 0 and self._data[j] > self._data[parent]):
            self._swap(j, parent)
            self._upheap(parent) # recur at position of parent

    def _downheap(self, j):
        if (self._has_left(j)):
            left = self._left(j)
            small_child = left # although right may be smaller
            if self._has_right(j):
                right = self._right(j)
                if self._data[right] > self._data[left]:
                    small_child = right
            if self._data[small_child] > self._data[j]:
                self._swap(j, small_child)
                self._downheap(small_child) # recur at position of small child
    
    def _bubble(self, j):
        if j > 0 and self._data[j] > self._data[self._parent(j)]:
            self._upheap(j)
        else:
            self._downheap(j)

#------------------------------ Public Functions ------------------------------

# self._data stores (vertex, priority) index wise in a list form
# self._refer stores (index in data list, dw) index wise in a list form
# If no index exists then index = -1
# All dw values initialised to 0 while constructing

    def __init__ (self, contents=()): # Constructor
        self._data = [] 
        self._refer = []
        for val in contents:
            obj = self._Node(val[0], val[1])
            self._refer.append((len(self._data), 0, -1))      # Attempt to store previous vertex
            self._data.append(obj)            
        if len(self._data) > 1:
            self._heapify()

    def _heapify(self):
        start = self._parent(len(self) - 1) # start at PARENT of last leaf
        for j in range(start, -1, -1): # going to and including the root
            self._downheap(j)

    def __len__ (self):
        return len(self._data)

    def _ExtractMax(self):
        # Retrieving the first & last elements and their dw values
        last = self._data[len(self._data)-1]
        ldw = self._refer[last._vertex][1]
        ldww = self._refer[last._vertex][2]

        item = self._data[0]
        zdw = self._refer[item._vertex][1]
        zdww = self._refer[item._vertex][2]
        self._refer[self._data[0]._vertex]=(-1, zdw, zdww)
        
        self._data[0] = last
        self._data.pop()

        self._refer[last._vertex] = (0, ldw, ldww)
        self._downheap(0)
        return (item._vertex, item._priority)

    # Takes the vertex & new priority as input
    def _update_heap(self, vertex, newdv):
        ver_ind = self._refer[vertex][0]
        new_node = self._Node(vertex, newdv)
        self._data[ver_ind] = new_node
        self._bubble(ver_ind)

    def _update_refer(self, vertex, newdw):
        index = self._refer[vertex][0]
        self._refer[vertex] = (index, newdw)
        return

#---------------------------------------- End Of Max Heap Data Structure ------------------------------------

# For Retrieving Refer List & Formatting to required Output
def Output(inp,s, t):
    C = inp[t][1]
    route = [t]
    i = t
    while (i != s):
        route.insert(0,inp[i][2])
        i = inp[i][2]
    return(C, route)

def findMaxCapacity(n, links, s, t):    # Returns (C, route)
    AdList = []
    Inp = []

    for i in range(0, n):
        AdList.append([])
        Inp.append((i, 0))

    for i in range(0,len(links)):
        AdList[links[i][0]].append((links[i][1], links[i][2]))
        AdList[links[i][1]].append((links[i][0], links[i][2]))
    
    MHeap = HeapPriorityQueue(Inp)
    MHeap._update_heap(s,'inf')

    while (len(MHeap._data)>0):
        v = MHeap._ExtractMax() # Vertex With Maximum Priority
        vertex = v[0]

        for i in range(0, len(AdList[vertex])):
            dList = MHeap._refer
        
            vert_nbr = AdList[vertex][i][0]         # Neighbour Vertex Name
            index_nbr = dList[vert_nbr][0]            # Neighbour Vertex Index in Data List 
            
            if (index_nbr != -1):                   # Making Sure The Vertex is in Data List
                dw_nbr = dList[vert_nbr][1]
                dw_prev = dList[vertex][1]       # The dw value of previous vertex
                weight = AdList[vertex][i][1]

                if (vertex == s): dw_prev = weight
                elif (weight <= dw_prev): dw_prev = weight 

                if (dw_prev >= dw_nbr):
                    MHeap._update_heap(vert_nbr, dw_prev)
                    MHeap._update_refer(vert_nbr, dw_prev)
                
                    a = MHeap._refer[vert_nbr][0]
                    b = MHeap._refer[vert_nbr][1]
                    MHeap._refer[vert_nbr] = (a,b,vertex)
            
    return(Output(MHeap._refer,s, t))
    



# Testcases
# print(findMaxCapacity(3,[(0,1,1),(1,2,1)],0,1))
# print(findMaxCapacity(4,[(0,1,30),(0,3,10),(1,2,40),(2,3,50),(0,1,60),(1,3,50)],0,3))
# print(findMaxCapacity(4,[(0,1,30),(1,2,40),(2,3,50),(0,3,10)],0,3))
# print(findMaxCapacity(5,[(0,1,3),(1,2,5),(2,3,2),(3,4,3),(4,0,8),(0,3,7),(1,3,4)],0,2))
# print(findMaxCapacity(7,[(0,1,2),(0,2,5),(1,3,4), (2,3,4),(3,4,6),(3,5,4),(2,6,1),(6,5,2)],0,5))
# print(findMaxCapacity(4,[(0,1,5),(0,2,3),(2,3,3),(3,1,3)],0,1))