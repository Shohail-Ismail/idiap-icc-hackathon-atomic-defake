from atomic_defake.atomic_defake import AtomicDeFake


adf = AtomicDeFake(aggregation_method="single_false_or_unsure")

post_text = "I am a cat."

result = adf.verify(post_text)

print(result)
