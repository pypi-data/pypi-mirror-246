import numpy as np

from ... import reg, aux
from ...param import Epoch

__all__ = [
    'Trial_dict',
    'Exp_dict',
]

def trial_conf(durs=[], qs=[]):
    cumdurs = np.cumsum([0] + durs)
    return aux.ItemList(
        Epoch(age_range=(t0,t1), sub=[q, 'standard']).nestedConf for
         i, (t0, t1, q) in enumerate(zip(cumdurs[:-1], cumdurs[1:], qs)))


@reg.funcs.stored_conf("Trial")
def Trial_dict():
    d = aux.AttrDict({
        'default': aux.AttrDict({'epochs' : trial_conf()}),
        'odor_preference': aux.AttrDict({'epochs' : trial_conf(
            [5.0] * 8,
            [1.0, 0.0] * 4)}),
        'odor_preference_short': aux.AttrDict({'epochs' : trial_conf(
            [0.125] * 8,
            [1.0, 0.0] * 4)})
    })
    return d


def grouped_exp_dic():
    from ...param.composition import Odor
    from ...reg import gen
    from ...reg.generators import GTRvsS

    def lg(id=None,**kwargs):
        l=reg.gen.LarvaGroup(**kwargs)
        if id is None:
            id=l.model
        return l.entry(id)

    def lgs(mIDs, ids=None, cs=None, **kwargs):
        if ids is None:
            ids = mIDs
        N = len(mIDs)
        if cs is None:
            cs = aux.N_colors(N)
        return aux.AttrDict(aux.merge_dicts([lg(id=id, c=c, mID=mID, **kwargs) for mID, c, id in zip(mIDs, cs, ids)]))

    def exp(id, env=None, l={}, en=reg.gen.EnrichConf(), dur=10.0,c=[], c0=['pose'], **kwargs):
        if env is None:
            env = id
        return gen.Exp(larva_groups=l, env_params=reg.conf.Env.get(env), experiment=id, enrichment=en, collections=c0 + c,duration=dur, **kwargs).nestedConf

    def food_exp(id, c=['feeder'], dur=10.0,
                 en=gen.EnrichConf(anot_keys=['bout_detection', 'bout_distribution', 'source_attraction'],
                                           proc_keys=['spatial', 'angular', 'source']), **kwargs):
        return exp(id, c=c,dur=dur, en=en,
                   **kwargs)

    def touch_exp(id, c=['toucher'], dur=600.0,
                 en=gen.EnrichConf(anot_keys=['bout_detection', 'bout_distribution', 'source_attraction'],
                                           proc_keys=['spatial', 'angular', 'source']), **kwargs):
        return exp(id, c=c,dur=dur, en=en,
                   **kwargs)

    def game_exp(id, dur=20.0, **kwargs):
        return exp(id, dur=dur, **kwargs)

    def deb_exp(id, dur=5.0,env='food_grid', **kwargs):
        return exp(id, dur=dur,env=env, c=['feeder', 'gut'],
                   en=gen.EnrichConf(proc_keys=['spatial'],anot_keys=[]), **kwargs)

    def thermo_exp(id, dur=10.0, **kwargs):
        return exp(id, dur=dur, c=['thermo'], **kwargs)

    def pref_exp(id, dur=5.0, **kwargs):
        return exp(id,dur=dur, en=gen.EnrichConf(proc_keys=['PI'],anot_keys=[]), **kwargs)

    def game_groups(dim=0.1, N=10, x=0.4, y=0.0, mode='king'):
        x = np.round(x * dim, 3)
        y = np.round(y * dim, 3)
        if mode == 'king':
            l = {**lg(id='Left', N=N, loc=(-x, y), mID='gamer-5x', c='darkblue', odor=Odor.oG(id='Left_odor')),
                 **lg(id='Right', N=N, loc=(+x, y), mID='gamer-5x', c='darkred', odor=Odor.oG(id='Right_odor'))}
        elif mode == 'flag':
            l = {**lg(id='Left', N=N, loc=(-x, y), mID='gamer', c='darkblue'),
                 **lg(id='Right', N=N, loc=(+x, y), mID='gamer', c='darkred')}
        elif mode == 'catch_me':
            l = {**lg(id='Left', N=1, loc=(-0.01, 0.0), mID='follower-L', c='darkblue', odor=Odor.oD(id='Left_odor')),
                 **lg(id='Right', N=1, loc=(+0.01, 0.0), mID='follower-R', c='darkred', odor=Odor.oD(id='Right_odor'))}
        return l

    def lgs_x4(N=5):
        return lgs(
            mIDs=['max_forager', 'max_feeder', 'navigator', 'explorer'],
            ids=['forager', 'Orco', 'navigator', 'explorer'], N=N)

    d0 = {
        'tethered': {'env': 'focus', 'dur': 30.0,
                     'l': lg(mID='immobile', N=1, ors=(90.0, 90.0))
                     },
        'focus': {
            'l': lg(mID='Levy', N=1, ors=(90.0, 90.0))
        },
        'dish': {
            'l': lg(mID='explorer', N=25, s=(0.02,0.02))
        },
        'dispersion': {'env': 'arena_200mm',
                       'l': lg(mID='explorer', N=25)
                       },
        'dispersion_x2': {'env': 'arena_200mm', 'dur': 3.0,
                          'l': lgs(mIDs=['explorer', 'Levy'], ids=['CoupledOsc', 'Levy'],
                                   N=5)
                          }
    }
    d00 = {id: exp(id=id, **kws) for id, kws in d0.items()}

    d1 = {
        'chemotaxis': {'env': 'odor_gradient', 'dur': 5.0,
                       'l': lg(mID='NEU_Levy_continuous_nav', N=8, loc=(-0.04, 0.0), s=(0.005, 0.02),
                               ors=(-30.0, 30.0))},
        'chemorbit': {'env': 'mid_odor_gaussian', 'dur': 3.0, 'l': lg(mID='navigator', N=3)},
        'chemorbit_OSN': {'env': 'mid_odor_gaussian', 'dur': 3.0, 'l': lg(mID='OSNnavigator', N=3)},
        'chemorbit_x2': {'env': 'mid_odor_gaussian', 'dur': 3.0,
                         'l': lgs(mIDs=['navigator', 'RLnavigator'],
                                  ids=['CoupledOsc', 'RL'], N=10)},
        'chemorbit_x4': {'env': 'odor_gaussian_square', 'dur': 3.0, 'l': lgs_x4()},
        'chemotaxis_diffusion': {'env': 'mid_odor_diffusion', 'l': lg(mID='navigator', N=30)},
        'chemotaxis_RL': {'env': 'mid_odor_diffusion',
                          'l': lg(mID='RLnavigator', N=10, mode='periphery', s=(0.04,0.04))},
        'reorientation': {'env': 'mid_odor_diffusion', 'l': lg(mID='immobile', N=200, s=(0.05,0.05))},
        'food_at_bottom': {'dur': 1.0,
                           'l': lgs(mIDs=['max_feeder', 'max_forager'],
                                    ids=['Orco', 'control'], N=5, sh='oval', loc=(0.0, 0.04), s=(0.04, 0.01))}
    }

    d11 = {id: exp(id=id, c0=['olfactor', 'pose'],
                   en=gen.EnrichConf(anot_keys=['bout_detection', 'bout_distribution', 'source_attraction'],
                                             proc_keys=['spatial', 'angular', 'source']),
                   **kws) for id, kws in d1.items()}

    d2 = {
        'anemotaxis': {'env': 'windy_arena', 'dur': 0.5, 'l': lg(mID='explorer', N=4)},
        'anemotaxis_bordered': {'env': 'windy_arena_bordered', 'dur': 0.5, 'l': lg(mID='explorer', N=4)},
        'puff_anemotaxis_bordered': {'env': 'puff_arena_bordered', 'dur': 0.5, 'l': lg(mID='explorer', N=4)},
    }

    d22 = {id: exp(id=id, c0=['wind', 'pose'],
                   en=gen.EnrichConf(proc_keys=['spatial', 'angular', 'wind']),
                   **kws) for id, kws in d2.items()}

    d3 = {
        'single_puff': {'env': 'single_puff', 'dur': 2.5,
                        'l': lg(mID='explorer', N=20)}
    }

    d33 = {id: exp(id=id, c0=['wind', 'olfactor', 'pose'],
                   en=gen.EnrichConf(anot_keys=['bout_detection', 'bout_distribution', 'source_attraction'],
                                             proc_keys=['spatial', 'angular', 'source', 'wind']),
                   **kws) for id, kws in d3.items()}

    d = {
        'exploration': d00,
        'chemotaxis': d11,
        'anemotaxis': d22,
        'chemanemotaxis': d33,

        'thermotaxis': {
            'thermotaxis': thermo_exp('thermotaxis', env='thermo_arena', l=lg(mID='thermo_navigator', N=10)),

        },

        'odor_preference': {
            'PItest_off': pref_exp('PItest_off', env='CS_UCS_off_food', dur=3.0,
                                   l=lg(N=25, s=(0.005, 0.02), mID='navigator_x2')),
            'PItest_off_OSN': pref_exp('PItest_off', env='CS_UCS_off_food', dur=3.0,
                                   l=lg(N=25, s=(0.005, 0.02), mID='OSNnavigator_x2')),
            'PItest_on': pref_exp('PItest_on', env='CS_UCS_on_food', l=lg(N=25, s=(0.005, 0.02), mID='forager_x2')),
            'PItrain_mini': pref_exp('PItrain_mini', env='CS_UCS_on_food_x2', dur=1.0, c=['olfactor'],
                                     trials=reg.conf.Trial.getID('odor_preference_short'), l=lg(N=25, s=(0.005, 0.02), mID='forager_RL')),
            'PItrain': pref_exp('PItrain', env='CS_UCS_on_food_x2', dur=41.0, c=['olfactor'],
                                trials=reg.conf.Trial.getID('odor_preference'), l=lg(N=25, s=(0.005, 0.02), mID='forager_RL')),
            'PItest_off_RL': pref_exp('PItest_off_RL', env='CS_UCS_off_food', dur=105.0, c=['olfactor'],
                                      l=lg(N=25, s=(0.005, 0.02), mID='RLnavigator'))},
        'foraging': {
            'patchy_food': food_exp('patchy_food', env='patchy_food', l=lg(mID='forager', N=25)),
            'patch_grid': food_exp('patch_grid', env='patch_grid', l=lgs_x4()),
            'MB_patch_grid': food_exp('MB_patch_grid', env='patch_grid', c=['feeder', 'olfactor'],
                                      l=lgs(mIDs=['max_forager0_MB', 'max_forager_MB'], N=3)),
            'noMB_patch_grid': food_exp('noMB_patch_grid', env='patch_grid', c=['feeder', 'olfactor'],
                                        l=lgs(mIDs=['max_forager0', 'max_forager'], N=4)),
            'random_food': food_exp('random_food', env='random_food', c=['feeder', 'toucher'],
                                    l=lgs(mIDs=['feeder', 'forager_RL'],
                                          ids=['Orco', 'RL'], N=5,mode='uniform',
                                          shape='rect', s=(0.04,0.04))),
            'uniform_food': food_exp('uniform_food', env='uniform_food',
                                     l=lg(mID='feeder', N=5, s=(0.005,0.005))),
            'food_grid': food_exp('food_grid', env='food_grid', l=lg(mID='feeder', N=5)),
            'single_odor_patch': food_exp('single_odor_patch', env='single_odor_patch',
                                          l=lgs(mIDs=['feeder', 'forager'],
                                                ids=['Orco', 'control'], N=5, mode='periphery', s=(0.01,0.01))),
            'single_odor_patch_x4': food_exp('single_odor_patch_x4', env='single_odor_patch', l=lgs_x4()),
            'double_patch': food_exp('double_patch', env='double_patch', l=GTRvsS(N=5),
                                     c=['toucher', 'feeder', 'olfactor'],
                                     en=reg.gen.EnrichConf(
                                         anot_keys=['bout_detection', 'bout_distribution', 'interference',
                                                    'patch_residency'],
                                         proc_keys=['spatial', 'angular', 'source'])),

            '4corners': exp('4corners', env='4corners', l=lg(mID='forager_RL', N=10, s=(0.04,0.04)))
        },

        'tactile' : {
            'tactile_detection': touch_exp('tactile_detection', env='single_patch',
                                          l=lg(mID='toucher', N=15, mode='periphery', s=(0.03, 0.03))),
            'tactile_detection_x4': touch_exp('tactile_detection_x4', env='single_patch',
                                             l=lgs(mIDs=['RLtoucher_2', 'RLtoucher', 'toucher', 'toucher_brute'],
                                                   ids=['RL_3sensors', 'RL_1sensor', 'control', 'brute'],
                                                   N=10)),

            'multi_tactile_detection': touch_exp('multi_tactile_detection', env='multi_patch',
                                                l=lgs(mIDs=['RLtoucher_2', 'RLtoucher', 'toucher'],
                                                      ids=['RL_3sensors', 'RL_1sensor', 'control'], N=4)),
        },

        'growth': {'growth': deb_exp('growth',  dur=24 * 60.0, l=GTRvsS(age=0.0)),
                   'RvsS': deb_exp('RvsS', dur=180.0, l=GTRvsS(age=0.0)),
                   'RvsS_on': deb_exp('RvsS_on',  dur=20.0, l=GTRvsS()),
                   'RvsS_off': deb_exp('RvsS_off', env='arena_200mm', dur=20.0, l=GTRvsS()),
                   'RvsS_on_q75': deb_exp('RvsS_on_q75',  l=GTRvsS(q=0.75)),
                   'RvsS_on_q50': deb_exp('RvsS_on_q50',  l=GTRvsS(q=0.50)),
                   'RvsS_on_q25': deb_exp('RvsS_on_q25',  l=GTRvsS(q=0.25)),
                   'RvsS_on_q15': deb_exp('RvsS_on_q15', l=GTRvsS(q=0.15)),
                   'RvsS_on_1h_prestarved': deb_exp('RvsS_on_1h_prestarved',  l=GTRvsS(h_starved=1.0)),
                   'RvsS_on_2h_prestarved': deb_exp('RvsS_on_2h_prestarved',  l=GTRvsS(h_starved=2.0)),
                   'RvsS_on_3h_prestarved': deb_exp('RvsS_on_3h_prestarved',  l=GTRvsS(h_starved=3.0)),
                   'RvsS_on_4h_prestarved': deb_exp('RvsS_on_4h_prestarved', l=GTRvsS(h_starved=4.0)),

                   },

        'games': {
            'maze': game_exp('maze', env='maze', c=['olfactor'],
                             l=lg(N=5, loc=(-0.4 * 0.1, 0.0), ors=(-60.0, 60.0), mID='navigator')),
            'keep_the_flag': game_exp('keep_the_flag', env='game', l=game_groups(mode='king')),
            'capture_the_flag': game_exp('capture_the_flag', env='game', l=game_groups(mode='flag')),
            'catch_me': game_exp('catch_me', env='arena_50mm_diffusion', l=game_groups(mode='catch_me'))
        },

        'zebrafish': {
            'prey_detection': exp('prey_detection', env='windy_blob_arena',
                                  l=lg(mID='zebrafish', N=4, s=(0.002, 0.005)),
                                  dur=20.0)
        },

        'other': {
            'realistic_imitation': exp('realistic_imitation', env='dish', l=lg(mID='imitator', N=25),
                                       Box2D=True, c=['midline', 'contour'])
            # 'imitation': imitation_exp('None.150controls', model='explorer'),
        }
    }

    return d


@reg.funcs.stored_conf("Exp")
def Exp_dict():
    exp_dict = aux.merge_dicts(list(grouped_exp_dic().values()))
    return exp_dict


