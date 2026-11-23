__int64 __fastcall sub_1401089B0(
        __int64 a1,
        _QWORD *a2,
        __int64 a3,
        __int64 a4,
        unsigned __int8 a5,
        unsigned __int8 a6,
        __int64 a7,
        int a8,
        unsigned __int8 a9)
{
  __int64 v13; // rax
  __int64 v14; // rdx
  volatile signed __int32 *v15; // rcx
  __int64 v16; // r8
  volatile signed __int32 *v17; // rbp
  volatile signed __int32 *v18; // rcx
  volatile signed __int32 *v19; // rcx
  __int64 v20; // rdi
  __int64 v21; // rdi
  __int64 v22; // rax
  __int64 v23; // rbx
  volatile signed __int32 *v24; // rcx
  __int64 v25; // rdi
  __int64 v26; // r8
  volatile signed __int32 *v27; // rcx
  volatile signed __int32 *v28; // rcx
  volatile signed __int32 *v29; // rbx
  int v30; // ebx
  __int64 v31; // r9
  unsigned __int8 v32; // al
  __int64 v33; // rdx
  __int64 v34; // rcx
  __int64 v35; // r8
  __int64 v36; // rax
  void (__fastcall ***v37)(_QWORD, __int64); // rcx
  void (__fastcall ***v38)(_QWORD, __int64); // rcx
  int v39; // ebp
  __int64 v40; // r9
  unsigned __int8 v41; // bl
  volatile signed __int32 *v42; // rcx
  volatile signed __int32 *v43; // rcx
  __int64 v44; // rax
  __int64 v45; // rax
  __int64 v46; // rax
  volatile signed __int32 *v48; // [rsp+40h] [rbp-138h] BYREF
  volatile signed __int32 *v49; // [rsp+48h] [rbp-130h] BYREF
  volatile signed __int32 *v50; // [rsp+50h] [rbp-128h] BYREF
  _BYTE v51[24]; // [rsp+58h] [rbp-120h] BYREF
  _QWORD v52[4]; // [rsp+70h] [rbp-108h] BYREF
  _QWORD v53[8]; // [rsp+90h] [rbp-E8h] BYREF
  char v54[168]; // [rsp+D0h] [rbp-A8h] BYREF

  sub_1407C9510(a1: v51);
  if ( (unsigned __int8)sub_1407D8B00(a1: a4, a2: &qword_141B598B8) == 0 )
  {
    sub_1407D0D60(a1: v52);
    sub_1407D0F70(a1: (unsigned int)v52, a2: (unsigned int)&v48, a3: (_DWORD)a2, a4: a3, a5: a4, a6: 0, a7: 0, a8: 0);
    v17 = v48;
    if ( v48 == nullptr )
      goto LABEL_36;
    if ( WORD2(v52[0]) < 6u )
    {
      v49 = v48;
      _InterlockedIncrement(v48 + 2);
      sub_1407CB960(a1: v53, a2: &v49);
      v27 = v48;
      if ( v48 == (volatile signed __int32 *)v53[0] )
      {
        if ( v48 != nullptr && _InterlockedDecrement(v48 + 2) == 0 )
          (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v27)(a1: v27, a2: 1);
      }
      else
      {
        if ( v48 != nullptr && _InterlockedDecrement(v48 + 2) == 0 )
          (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v27)(a1: v27, a2: 1);
        v48 = (volatile signed __int32 *)v53[0];
        v53[0] = 0;
      }
      v28 = v49;
      if ( v49 != nullptr && _InterlockedDecrement(v49 + 2) == 0 )
        (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v28)(a1: v28, a2: 1);
      v29 = v48;
      (*(void (__fastcall **)(volatile signed __int32 *, _QWORD *, __int64))(*(_QWORD *)v48 + 40LL))(
        a1: v48,
        a2: v53,
        a3: 1);
      if ( *((_DWORD *)v29 + 4) == 0 )
      {
        v30 = 1;
        if ( LOBYTE(v53[0]) != 0 )
          goto LABEL_32;
        goto LABEL_48;
      }
    }
    else
    {
      (*(void (__fastcall **)(volatile signed __int32 *, volatile signed __int32 **, __int64))(*(_QWORD *)v48 + 40LL))(
        a1: v48,
        a2: &v50,
        a3: 1);
      if ( *((_DWORD *)v17 + 4) == 0 && (_BYTE)v50 == 0 )
      {
        v49 = v48;
        if ( v48 != nullptr )
          _InterlockedIncrement(v48 + 2);
        sub_1407CC0B0(a1: v53, a2: &v49);
        v18 = v48;
        if ( v48 == (volatile signed __int32 *)v53[0] )
        {
          if ( v48 != nullptr && _InterlockedDecrement(v48 + 2) == 0 )
            (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v18)(a1: v18, a2: 1);
        }
        else
        {
          if ( v48 != nullptr && _InterlockedDecrement(v48 + 2) == 0 )
            (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v18)(a1: v18, a2: 1);
          v48 = (volatile signed __int32 *)v53[0];
          v53[0] = 0;
        }
        v19 = v49;
        if ( v49 != nullptr && _InterlockedDecrement(v49 + 2) == 0 )
          (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v19)(a1: v19, a2: 1);
LABEL_48:
        v53[0] = v48;
        if ( v48 != nullptr )
          _InterlockedIncrement(v48 + 2);
        sub_140803850(a1: &v49, a2: v53, a3: 0x10000);
        v38 = (void (__fastcall ***)(_QWORD, __int64))v53[0];
        if ( v53[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v53[0] + 8LL)) == 0 )
          (**v38)(a1: v38, a2: 1);
        sub_1407C9510(a1: v53);
        sub_140839290(a1: v49, a2: &v50, a3: v53);
        v39 = (int)v50;
        v30 = 1;
        if ( (*(unsigned __int8 (__fastcall **)(__int64, _QWORD *))(*(_QWORD *)a1 + 160LL))(a1, a2: v53) != 0
          && v39 == 0 )
        {
          v40 = WORD2(v52[0]);
          v50 = v49;
          if ( v49 != nullptr )
            _InterlockedIncrement(v49 + 2);
          v41 = (*(__int64 (__fastcall **)(__int64, _BYTE *, volatile signed __int32 **, __int64))(*(_QWORD *)a1 + 144LL))(
                  a1,
                  a2: v51,
                  a3: &v50,
                  a4: v40);
          v42 = v50;
          if ( v50 != nullptr && _InterlockedDecrement(v50 + 2) == 0 )
            (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v42)(a1: v42, a2: 1);
          v30 = v41 ^ 1;
        }
        sub_140833970(a1: v53);
        v43 = v49;
        if ( v49 != nullptr && _InterlockedDecrement(v49 + 2) == 0 )
          (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v43)(a1: v43, a2: 1);
LABEL_32:
        v15 = v48;
        if ( v48 != nullptr && _InterlockedDecrement(v48 + 2) == 0 )
          (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v15)(a1: v15, a2: 1);
        if ( v30 == 0 )
          goto LABEL_37;
LABEL_36:
        LODWORD(a2) = 0;
        goto LABEL_67;
      }
    }
    v30 = 1;
    goto LABEL_32;
  }
  sub_140149E70(a1: v53);
  v53[0] = 0x141763368LL;
  sub_1400D9D50(a1: v54, a2: v52, a3: &qword_141B5C860);
  *(_QWORD *)(v52[0] + 40LL) = sub_1400D9CF0;
  if ( (unsigned __int8)sub_14084AD10(a1: v53, a2, a3, a4) != 0 )
  {
    v13 = sub_1402ECE80(a1: v53);
    sub_140834E80(a1: v51, a2: v13);
    sub_140844F40(a1: v53);
LABEL_37:
    v31 = a6;
    if ( a8 != 4 )
    {
      v32 = sub_140034150(a1: v15, a2: v14, a3: v16, a4: a6);
      v31 = a6;
      if ( ((a9 ^ 1) & v32) == 0 && a5 == 0 )
      {
        if ( (unsigned __int8)sub_140034150(a1: v34, a2: v33, a3: v35, a4: a6) != 0 )
        {
          (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a2 + 120LL))(a1: *a2, a2: v52);
          v36 = sub_140843600();
          sub_1408436D0(a1: v36, a2: v53, a3: v52);
          sub_140835380(a1: v51, a2: 1718578276, a3: v53);
          sub_14083D320(a1: v53);
          v37 = (void (__fastcall ***)(_QWORD, __int64))v52[0];
          if ( v52[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v52[0] + 8LL)) == 0 )
            (**v37)(a1: v37, a2: 1);
        }
        else
        {
          v44 = sub_140843600();
          sub_1408436D0(a1: v44, a2: v53, a3: a2);
          sub_140835380(a1: v51, a2: 1718578276, a3: v53);
          sub_14083D320(a1: v53);
        }
        v45 = sub_1400015F0(a1: a3);
        sub_14083D970(a1: v53, a2: v45);
        sub_140835380(a1: v51, a2: 1718185061, a3: v53);
        sub_14083D320(a1: v53);
        v46 = sub_140179440(a1: a4);
        a2 = v53;
        sub_14083D970(a1: v53, a2: v46);
        sub_140835380(a1: v51, a2: 1179407449, a3: v53);
        sub_14083D320(a1: v53);
        v31 = a6;
      }
    }
    (*(void (__fastcall **)(__int64, _BYTE *, _QWORD, __int64, __int64, int, __int64))(*(_QWORD *)a1 + 384LL))(
      a1,
      a2: v51,
      a3: a5,
      a4: v31,
      a5: a7,
      a6: a8,
      a7: a4);
    LOBYTE(a2) = 1;
    goto LABEL_67;
  }
  v20 = qword_141ABD468;
  v48 = nullptr;
  sub_140809040(a1: &v48, a2: 0x141927D92LL, a3: 0xFFFFFFFFLL);
  sub_140824A20(a1: v20, a2: v52, a3: &v48);
  sub_140808B00(a1: &v48);
  v21 = sub_1400015F0(a1: a3);
  v22 = sub_1407E4940();
  v23 = sub_1407E4490(a1: v22, a2: 24);
  *(_DWORD *)(v23 + 8) = 0;
  *(_QWORD *)v23 = 0x141759568LL;
  *(_QWORD *)(v23 + 16) = 0;
  sub_140809100(a1: v23 + 16, a2: v21);
  v48 = (volatile signed __int32 *)v23;
  _InterlockedIncrement((volatile signed __int32 *)(v23 + 8));
  sub_14081D7C0(a1: v52, a2: 1, a3: &v48, a4: 0);
  v24 = v48;
  if ( v48 != nullptr && _InterlockedDecrement(v48 + 2) == 0 )
    (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v24)(a1: v24, a2: 1);
  v25 = qword_141B5AD60;
  LODWORD(a2) = 0;
  sub_14081ED40(a1: v52, a2: &v48, a3: 0);
  LOBYTE(v26) = 1;
  (*(void (__fastcall **)(__int64, volatile signed __int32 **, __int64, _QWORD))(*(_QWORD *)v25 + 120LL))(
    a1: v25,
    a2: &v48,
    a3: v26,
    a4: 0);
  sub_140808B00(a1: &v48);
  sub_14081D040(a1: v52);
  sub_140844F40(a1: v53);
LABEL_67:
  sub_140833970(a1: v51);
  return (unsigned int)a2;
}
