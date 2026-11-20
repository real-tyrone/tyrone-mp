from pathlib import Path

root = Path(__file__).resolve().parents[1]
path = root / 'common/subject_types/tyrone_qing_administrations.txt'
text = path.read_text(encoding='utf-8')
start = text.index('subject_type_qing_frontier_administration = {')
text = text[:start] + text[start:].replace('can_target_with_transfer_wargoal = no', 'can_target_with_transfer_wargoal = yes', 1)
path.write_text(text, encoding='utf-8')
game = Path('C:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game')
path = root / 'common/war_goal_types/26_transfer_subject.txt'
text = (game / 'common/war_goal_types/26_transfer_subject.txt').read_text(encoding='utf-8-sig')
text = text.replace('on_enforced = {', '''on_enforced = {
        scope:target_country = {
            chi_qing_normalize_transferred_frontier = yes
        }''', 1)
path.write_text(text, encoding='utf-8')
