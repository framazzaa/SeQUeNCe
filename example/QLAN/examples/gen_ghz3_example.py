################################################################################
# Simple generation of a GHZ state in a three node network.
# - (Protocol = False -- ideal) the state is generated without distribution.
# - (Protocol = True -- circuit) the state is generated with qcircuit.
################################################################################

# Basic components
from sequence.kernel.timeline import Timeline
from sequence.topology.node import Node
from sequence.components.memory import Memory

# Log utility
import sequence.utils.log as log
from sequence.utils import log

from ..local_ghz_protocol import LocalGHZ3protocol


class GHZStateManager:
    """
    This class represents a GHZ state manager that keeps track of the entangled and empty memories.
    It provides methods to update the state of the memories and create a protocol for the owner.

    Attributes:
        owner (object): The owner object.
        memory1_name (str): The name of the first memory.
        memory2_name (str): The name of the second memory.
        memory3_name (str): The name of the third memory.
        raw_counter (int): The counter for the number of RAW states.
        ent_counter (int): The counter for the number of entangled states.
    """

    def __init__(self, owner, memory1_name, memory2_name, memory3_name):
        """
        Initializes a new instance of the GHZStateManager class.

        Args:
            owner (object): The owner object.
            memory1_name (str): The name of the first memory.
            memory2_name (str): The name of the second memory.
            memory3_name (str): The name of the third memory.
        """
        self.owner = owner
        self.memory1_name = memory1_name
        self.memory2_name = memory2_name
        self.memory3_name = memory3_name
        self.raw_counter = 0
        self.ent_counter = 0

    def update(self, protocol, memories: list, states: list):
        """
        Updates the number of entangled and empty memories based on the state.

        Args:
            protocol: The protocol object.
            memories (list): The list of memories.
            states (list): The list of states.
        """
        for i in range(len(memories)):
            if states[i] == 'RAW':
                self.raw_counter += 1
                memories[i].reset()
            else:
                self.ent_counter += 1

    def create_protocol(self):
        """
        Sets the memories of the manager equal to the owner's memories and sets the owner's protocol to LocalGHZprotocol.
        """
        memo1 = self.owner.components[self.memory1_name]
        memo2 = self.owner.components[self.memory2_name]
        memo3 = self.owner.components[self.memory3_name]

        self.owner.protocols = [LocalGHZ3protocol(self.owner, 'LocalGHZprotocol', memo1, memo2, memo3)]

################################################################################
# GHZnode: network node that shares a GHZ state. It inherits from the class "Node" then adds the memories as components and the simple manager.
################################################################################

class GHZnode(Node):
    """
    This class represents a network node that shares a GHZ state.
    It inherits from the class "Node" and adds the memories as components and the simple manager.

    Attributes:
        name (str): The name of the node.
        tl (Timeline): The timeline object.
    """
    def __init__(self, name: str, tl: Timeline):
        """
        Initializes a new instance of the GHZnode class.

        Args:
            name (str): The name of the node.
            tl (Timeline): The timeline object.
        """
        super().__init__(name, tl)
        
        # Instantiating memories
        memory1_name = '%s.memo1' % name
        memory2_name = '%s.memo2' % name
        memory3_name = '%s.memo3' % name
        
        memo1 = Memory(name=memory1_name, timeline=tl, fidelity=0.9, frequency=2000, efficiency=1, coherence_time=-1, wavelength=500)
        memo2 = Memory(name=memory2_name, timeline=tl, fidelity=0.9, frequency=2000, efficiency=1, coherence_time=-1, wavelength=500)
        memo3 = Memory(name=memory3_name, timeline=tl, fidelity=0.9, frequency=2000, efficiency=1, coherence_time=-1, wavelength=500)
        # Adding memories components
        self.add_component(memo1)
        self.add_component(memo2)
        self.add_component(memo3)
        # Adding resource manager
        self.resource_manager = GHZStateManager(owner=self,
                                               memory1_name = memory1_name, memory2_name = memory2_name, memory3_name = memory3_name)
    # Function for receiving classing messages using the chosen protocol
    # def receive_message(self, src: str, msg: "Message"):
    #    self.protocols[0].received_message(src, msg)
   
def entangle_memory(tl: Timeline, memo1: Memory, memo2: Memory, memo3: Memory, fidelity: float):
    """
    Entangles three memories to create a GHZ state.

    Args:
        tl (Timeline): The timeline object.
        memo1 (Memory): The first memory object.
        memo2 (Memory): The second memory object.
        memo3 (Memory): The third memory object.
        fidelity (float): The fidelity of the quantum state.

    Returns:
        None
    """

    # square root of 1/2
    SQRT_HALF = 0.5 ** 0.5

    # 1/sqrt(2)|000> + 0 +...+ 0 + 1/sqrt(2)|111>
    ghz_state = [SQRT_HALF, 0, 0, 0, 0, 0, 0, SQRT_HALF]

    # Resetting the memories
    memo1.reset()
    memo2.reset()
    memo3.reset()
    
    # Setting the memories (the memory keys) to the state GHZ:
    tl.quantum_manager.set([memo1.qstate_key, memo2.qstate_key, memo3.qstate_key], ghz_state)

    # Specifying to memo1, who is the entanglement partner (telling node_id and memo_id)
    memo1.entangled_memory['node1_id'] = memo2.owner.name
    memo1.entangled_memory['node1_id'] = memo3.owner.name

    memo1.entangled_memory['memo1_id'] = memo2.name
    memo1.entangled_memory['memo1_id'] = memo3.name

    # Same for memo2, whose partner is memo1
    memo2.entangled_memory['node1_id'] = memo1.owner.name
    memo2.entangled_memory['node1_id'] = memo3.owner.name
    memo2.entangled_memory['memo2_id'] = memo1.name
    memo2.entangled_memory['memo2_id'] = memo3.name

    # memories sharing entanglement must share the same fidelity for the quantum state:
    memo1.fidelity = memo2.fidelity = memo3.fidelity = fidelity

def run_experiment(tl, memo_1, memo_2, memo_3, use_protocol):
    """
    Run the experiment with the specified timeline and memories.

    Args:
        tl (Timeline): The timeline object.
        memo_1 (Memory): The first memory object.
        memo_2 (Memory): The second memory object.
        memo_3 (Memory): The third memory object.
        use_protocol (bool): Flag indicating whether to use the protocol or not.
    """
    tl.init()

    if use_protocol:
        # Create and start the protocol
        node1.resource_manager.create_protocol()
        node1.protocols[0].start()
    else:
        # Entangle the memories without using the protocol
        for i in range(10):
            entangle_memory(tl, memo_1, memo_2, memo_3, 0.9)

    tl.run()

def display_state_information(tl, memo_1, memo_2, memo_3):
    """
    Display the state information of the given memories and the corresponding quantum states stored in the quantum manager.

    Args:
        tl (Timeline): The timeline object.
        memo_1 (Memory): The first memory object.
        memo_2 (Memory): The second memory object.
        memo_3 (Memory): The third memory object.
    """
    # Print the state information of each memory
    print(memo_1.name, memo_1.entangled_memory, memo_1.fidelity)
    print(memo_2.name, memo_2.entangled_memory, memo_2.fidelity)
    print(memo_3.name, memo_3.entangled_memory, memo_3.fidelity)
    
    # Print the quantum states stored in each memory
    print(f"Quantum state stored in memory{memo_1.qstate_key+1}:\n {tl.quantum_manager.states[0]}")
    print(f"Quantum state stored in memory{memo_2.qstate_key+1}:\n {tl.quantum_manager.states[1]}")
    print(f"Quantum state stored in memory{memo_3.qstate_key+1}:\n {tl.quantum_manager.states[2]}")

################################################################################
# MAIN PROCESS:
# 1. Instantiate the timeline and nodes.
# 2. Create the communication channel.
# 3. Initialize quantum memories and configure settings.
# 4. Set up the resource manager for node operations.
# 5. Establish connections between nodes.
# 6. Activate protocols and begin the simulation.
################################################################################
if __name__ == '__main__':

    tl = Timeline()
    node1 = GHZnode('node1', tl)
    node1.set_seed(28)

    memo_1 = node1.components[node1.resource_manager.memory1_name]
    memo_2 = node1.components[node1.resource_manager.memory2_name]
    memo_3 = node1.components[node1.resource_manager.memory3_name]

    # Dynamically decide to use the protocol or not. This could be based on user input, configuration, etc.
    run_experiment(tl=tl, memo_1=memo_1, memo_2=memo_2, memo_3=memo_3, use_protocol=True)
    display_state_information(tl=tl, memo_1=memo_1, memo_2=memo_2, memo_3=memo_3)


    
    
    