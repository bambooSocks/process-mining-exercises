class Place():

    def __init__(self, name):
        self.name = name
        self.marking = 0

    def mark(self):
        self.marking += 1

    def isMarked(self):
        return self.marking > 0

    def unmark(self):
        if self.isMarked():
            self.marking -= 1
        else:
            print("Place", self.name, "has not tokens to be unmarked")

class Transition():

    def __init__(self, name, id):
        self.name = name
        self.id = id
        self._input = []
        self._output = []

    def isEnabled(self):
        return all(i.isMarked() for i in self._input)

    def addInputPlace(self, place):
        self._input.append(place)

    def addOutputPlace(self, place):
        self._output.append(place)

    def fire(self):
        if self._input == []:
            print("The transition", self.id, "has not inputing place")
            return
        if self._output == []:
            print("The transition", self.id, "has not outputing place")
            return
        
        if self.isEnabled():
            for i in self._input:
                i.unmark()
            for o in self._output:
                o.mark()
        else:
            print("The transition cannot be activated")
            return

class PetriNet():

    def __init__(self):
        self._places = []
        self._transitions = []

    def add_place(self, name):
        self._places.append(Place(name))

    def add_transition(self, name, id):
        self._transitions.append(Transition(name, id))

    def _find_place(self, place_name):
        place = None
        for p in self._places:
            if p.name == place_name:
                place = p
                break
        # if place == None:
        #     print("Place", place_name, "is not defined in the petri net")
        return place

    def _find_transition(self, transition_id):
        transition = None
        for t in self._transitions:
            if t.id == transition_id:
                transition = t
                break
        # if transition == None:
        #     print("Transition", transition_id, "is not defined in the petri net")
        return transition

    def add_edge(self, source, target):
        if self._find_place(source) == None:
            # source is transition
            transition = self._find_transition(source)
            if transition != None:
                # target is place
                place = self._find_place(target)
                if place != None:
                    transition.addOutputPlace(place)
        else:
            # source is place
            place = self._find_place(source)
            if place != None:
                # target is transition
                transition = self._find_transition(target)
                if transition != None:
                    transition.addInputPlace(place)
        return self

    def get_tokens(self, place_name):
        place = self._find_place(place_name)
        return place.marking if place != None else -1


    def is_enabled(self, transition_id):
        transition = self._find_transition(transition_id)
        return transition.isEnabled() if transition != None else False

    def add_marking(self, place_name):
        place = self._find_place(place_name)
        if place != None: 
            place.mark()

    def fire_transition(self, transition_id):
        transition = self._find_transition(transition_id)
        if transition != None: 
            transition.fire()
