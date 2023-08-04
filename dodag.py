import time
import random

class Node:
    all_instances= []
    def __init__(self, id):
        Node.all_instances.append(self)
        self.id = id
        self.parent = None
        self.children = []
        self.messages_received= 0
        self.messages_sent= 0
        self.messages_generated= 0

        
    def add_child(self, child):
        self.children.append(child)
        child.parent = self
        
    
class DODAG:
    def __init__(self, root_id):
        self.nodes = {}
        self.root_id = root_id
        self.root = Node(root_id)
        self.nodes[root_id] = self.root
        self.total_messages_received = 0
        
    def add_node(self, id, parent_id):
        if id in self.nodes:
            return
        node = Node(id)
        self.nodes[id] = node
        parent = self.nodes[parent_id]
        parent.add_child(node)
        
    def generate_messages(self, num_messages):
        nodes = list(self.nodes.values())
        sources = [n for n in nodes if n != self.root]
        for i in range(num_messages):
            source = random.choice(sources)
            source.messages_generated+= 1
            message = {'source': source.id, 'seq_num': i}
            self.deliver_message(message)
            time.sleep(0.001)
            
    def deliver_message(self, message):
        node = self.nodes[message['source']]
        while node != self.root:
            node.messages_sent+= 1
            node = node.parent
            node.messages_received+= 1

        self.total_messages_received += 1
        print(f"Message {message['seq_num']} delivered to root node")
        
    def add_nodes(self, num_nodes):
        for i in range(2, num_nodes + 1):
            parent_id = random.randint(1, i-1)
            self.add_node(i, parent_id)

    


if __name__ == '__main__':
    dodag = DODAG(1)
    f = open("dodag100.txt", "w")
    total_nodes=int(input("Enter no of nodes : "))
    f.writelines("Total number of nodes : " + str(total_nodes)+'\n')
    dodag.add_nodes(total_nodes)
    total_messages=int(input("Enter no of messages : "))
    f.writelines("Total number of packets generated: " + str(total_messages)+'\n')
    f.writelines("\n")

    dodag.generate_messages(total_messages)
    for obj in Node.all_instances:
        sent=str(obj.messages_sent)
        received=str(obj.messages_received)
        node=str(obj.id)
        generated=str(obj.messages_generated)
        f.writelines( "Node " + node + " generated packets = "+ generated +"\n")
        f.writelines( "Node " + node + " received packets = "+ received+"\n")
        f.writelines( "Node " + node + " sent packets = "+sent+"\n")
        f.writelines("\n")

    print(f"{dodag.total_messages_received} out of {total_messages} messages reached the root node")
    f.writelines("Total number of packets delivered to root node : " + str(dodag.total_messages_received)+'\n')
    overall_delivery_ratio=(dodag.total_messages_received/total_messages)*100
    f.writelines("Overall_delivery_ratio is : " + str(overall_delivery_ratio) + "%"+'\n')
    f.writelines("Propagation delay is : " + str(1*total_messages)+"ms" +'\n')


