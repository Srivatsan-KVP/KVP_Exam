import uuid, random, json, utils
from django.contrib.auth.models import User
from . import models


def getSeating(data: list[models.Room]) -> dict[str, list[dict[str, tuple[int, int]]]]:
    group_classes: dict[int, list[models.Room]] = {}
    for room in data:
        group_classes[room.group] = group_classes.get(room.group, [])
        group_classes[room.group].append(room)

    pairs: list[tuple[list[models.Room], list[models.Room]]] = []
    for classes in group_classes.values():
        l: list[models.Room] = []
        for _ in range(len(classes)):
            idx = random.randint(0, len(data)-1)
            l.append(data[idx])
            data.pop(idx)
        pairs.append((classes, l))

    res: dict[str, list[dict[str, tuple[int, int]]]] = {}
    for pair in pairs:
        idx = 0
        for room in pair[0]:
            i, roll = idx, 1
            while roll < room.strength:
                res[str(pair[1][i])] = res.get(str(pair[1][i]), [])
                res[str(pair[1][i])].append({ str(room): (roll, min(room.strength, roll+19)) })

                roll += 20
                i = (i+1) % len(pair[1])

            idx = (idx+2) % len(pair[1])

    return res


# CRUD 

def addSubject(uid: uuid.UUID | None, name: str) -> dict:
    if uid:
        models.Subject.objects.filter(uid=uid).update(name=name)
        return { 'valid': True }
    
    subj = models.Subject(name=name)
    subj.save()
    return { 'valid': True, 'uid': subj.uid.hex }


def addClass(uid: uuid.UUID | None, name: str, strength: int, group: int) -> dict:
    if uid:
        models.Room.objects.filter(uid=uid).update(
            name=name, strength=strength, group=group
        )
        return { 'valid': True }
    
    room = models.Room(name=name, strength=strength, group=group)
    room.save()
    return { 'valid': True, 'uid': room.uid.hex }


def addTeacher(extra: dict) -> dict:
    if len(User.objects.filter(username=extra['username'])) > 0:
        return { 'valid': False, 'message': 'Username already taken!' }
    
    user = User(username=extra['username'])
    user.set_password(extra['password'])
    user.save()

    teacher = models.Teacher(name=extra['name'], user=user)
    teacher.save()
    return { 'valid': True, 'uid': teacher.uid.hex }


def addLink(uid: uuid.UUID | None, extra: dict) -> dict:
    if uid:
        models.Link.objects.filter(uid=uid).update(
            teacher=models.Teacher.objects.get(uid=uuid.UUID(extra['teacher'])),
            subject=models.Subject.objects.get(uid=uuid.UUID(extra['subject'])),
        )
        return { 'valid': True }
    
    link = models.Link(
        room=models.Room.objects.get(uid=uuid.UUID(extra['room'])),
        teacher=models.Teacher.objects.get(uid=uuid.UUID(extra['teacher'])),
        subject=models.Subject.objects.get(uid=uuid.UUID(extra['subject'])),
    )
    link.save()
    return { 'valid': True, 'uid': link.uid.hex }


def addExam(data: dict) -> dict:
    uids = [uuid.UUID(i) for i in json.loads(data['uids'])]
    utils.saveDict(getSeating([models.Room.objects.get(uid=uid) for uid in uids]), data['date'])

    return { 'valid': True, 'url': f'/saved/{data["date"]}/' }

def addEntry(data: dict, date) -> dict:
    print('came here!')
    room = models.Room.objects.get(uid=data['uid'])

    if len(models.Entry.objects.filter(room=room, date=date)) == 0:
        models.Entry(room=room, date=date).save()

    entry = models.Entry.objects.get(room=room, date=date)
    absent = [int(i) for i in data['absent'].split()]
    
    if entry.absent:
        for roll in entry.absent.split():
            if int(roll) not in absent:
                absent.append(int(roll))

    absent.sort()
    entry.absent = ' '.join([str(i) for i in absent])
    entry.save()

    return { 'valid': True, 'class': room.name }