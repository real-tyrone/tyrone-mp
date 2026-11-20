"""Refresh only the coverage report after additional scoped trigger definitions."""
import generate_chi_adm_imperial_law_laws as generator
original=generator.write
def write(path,text):
    if str(path).endswith('docs/chi_adm_imperial_law_coverage.md'):
        (generator.ROOT/path).write_text(text,encoding='utf-8')
    else:
        original(path,text)
generator.CHECK=True
generator.write=write
generator.main()
