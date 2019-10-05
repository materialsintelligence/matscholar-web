

def get_counting_callbacks():
    materials = 'animatedCount("count-materials", countTime);'
    entities = 'animatedCount("count-entities", countTime);'
    abstracts = 'animatedCount("count-abstracts", countTime);'
    return materials + entities + abstracts
