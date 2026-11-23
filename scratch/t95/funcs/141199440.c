__int64 __fastcall sub_141199440(_QWORD *a1, _QWORD *a2, __int64 a3, int a4, int a5, int a6, char a7, __int64 a8)
{
  __int64 v11; // rsi
  __int64 v12; // rsi
  __int64 v13; // rsi
  __int64 v14; // rsi
  int v15; // ebp
  __int64 v16; // rsi
  __int64 v17; // rsi
  __int64 v18; // rsi
  __int64 v19; // rsi
  __int64 v20; // rsi
  int v21; // esi
  __int64 v22; // r14
  __int64 v23; // rax
  __int64 *v24; // r15
  __int64 v25; // rbp
  unsigned __int64 v26; // rcx
  unsigned __int64 v27; // r12
  unsigned __int64 v28; // rdx
  unsigned __int64 v29; // r12
  __int64 v30; // rsi
  __int64 v31; // rbp
  __int64 v32; // rdx
  __int64 v33; // rdx
  __int64 v34; // rsi
  __int64 v36; // rsi
  __int64 v37; // rsi
  __int64 v38; // rsi
  __int64 v39; // rsi
  __int64 v40; // rsi
  unsigned __int8 v41; // [rsp+41h] [rbp-67h] BYREF
  char v42; // [rsp+42h] [rbp-66h] BYREF
  char v43; // [rsp+43h] [rbp-65h] BYREF
  int v44; // [rsp+44h] [rbp-64h]
  __int64 *v45; // [rsp+48h] [rbp-60h]
  unsigned __int64 v46; // [rsp+50h] [rbp-58h]
  char v47[4]; // [rsp+5Ch] [rbp-4Ch] BYREF
  char v48[4]; // [rsp+60h] [rbp-48h] BYREF
  char v49[68]; // [rsp+64h] [rbp-44h] BYREF

  sub_141199360();
  v11 = *a2;
  (*(void (__fastcall **)(_QWORD, _QWORD *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 9, 4);
  if ( *(_DWORD *)(v11 + 16) != 0 )
    return 0;
  v12 = *a2;
  (*(void (__fastcall **)(_QWORD, _QWORD *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 7, 4);
  if ( *(_DWORD *)(v12 + 16) != 0 )
    return 0;
  v13 = *a2;
  (*(void (__fastcall **)(_QWORD, _QWORD *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 8, 4);
  if ( *(_DWORD *)(v13 + 16) != 0 )
    return 0;
  v14 = *a2;
  if ( *a2 != 0 )
  {
    _InterlockedIncrement((volatile signed __int32 *)(v14 + 8));
    (*(void (__fastcall **)(__int64, _QWORD *, __int64))(*(_QWORD *)v14 + 40LL))(v14, a1 + 10, 4);
  }
  v15 = *(_DWORD *)(v14 + 16);
  if ( _InterlockedDecrement((volatile signed __int32 *)(v14 + 8)) == 0 )
    (**(void (__fastcall ***)(__int64, __int64))v14)(v14, 1);
  if ( v15 != 0 )
    return 0;
  v16 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, (__int64)a1 + 84, 4);
  if ( *(_DWORD *)(v16 + 16) != 0 )
    return 0;
  v17 = *a2;
  (*(void (__fastcall **)(_QWORD, _QWORD *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 11, 1);
  if ( *(_DWORD *)(v17 + 16) != 0 )
    return 0;
  v18 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, (__int64)a1 + 89, 1);
  if ( *(_DWORD *)(v18 + 16) != 0 )
    return 0;
  v19 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, (__int64)a1 + 90, 1);
  if ( *(_DWORD *)(v19 + 16) != 0 )
    return 0;
  v20 = *a2;
  (*(void (__fastcall **)(_QWORD, unsigned __int8 *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, &v41, 1);
  if ( *(_DWORD *)(v20 + 16) != 0 )
    return 0;
  if ( v41 != 0 )
  {
    v21 = 0;
    do
    {
      v22 = sub_140F73400(136);
      *(_QWORD *)(v22 + 8) = -1;
      *(_DWORD *)(v22 + 16) = 0;
      *(_QWORD *)v22 = 0x141883D28LL;
      v23 = qword_141ABD470;
      if ( qword_141ABD470 == 0 )
      {
        v23 = sub_1407E4940();
        qword_141ABD470 = v23;
      }
      *(_QWORD *)(v22 + 96) = 0;
      *(_QWORD *)(v22 + 88) = 0;
      *(_QWORD *)(v22 + 80) = 0;
      *(_QWORD *)(v22 + 72) = 0;
      *(_QWORD *)(v22 + 64) = 0;
      *(_QWORD *)(v22 + 56) = 0;
      *(_QWORD *)(v22 + 48) = 0;
      *(_QWORD *)(v22 + 40) = 0;
      *(_QWORD *)(v22 + 32) = 0;
      *(_QWORD *)(v22 + 24) = 0;
      *(_QWORD *)(v22 + 104) = 124518401;
      *(_DWORD *)(v22 + 112) = 0;
      *(_QWORD *)(v22 + 116) = 0x76C0001076C0001LL;
      *(_WORD *)(v22 + 124) = 0;
      *(_DWORD *)(v22 + 126) = -16384000;
      *(_WORD *)(v22 + 130) = 255;
      *(_BYTE *)(v22 + 132) = 0;
      v24 = (__int64 *)a1[4];
      if ( v24 == (__int64 *)a1[5] )
      {
        v44 = v21;
        v25 = (__int64)v24 - a1[3];
        v26 = v25 >> 3;
        v27 = (unsigned __int64)(v25 >> 3) >> 1;
        v28 = 0x1FFFFFFFFFFFFFFFLL - v27;
        v29 = (v25 >> 3) + v27;
        v46 = (v25 >> 3) + 1;
        v30 = v25;
        if ( v29 <= v46 )
          v29 = v26 + 1;
        if ( v26 > v28 )
          v29 = 0x1FFFFFFFFFFFFFFFLL;
        v31 = sub_1407E4490(v23, 8 * v29);
        *(_QWORD *)(v31 + v30) = v22;
        v32 = a1[3];
        v45 = (__int64 *)a1[4];
        sub_141758A00(v31, v32, (char *)v24 - v32);
        if ( v45 != v24 )
          sub_141758A00(v31 + v30 + 8, v24, a1[4] - (_QWORD)v24);
        v33 = a1[3];
        v21 = v44;
        if ( v33 != 0 )
          sub_1407E4890(qword_141ABD470, v33, a1[5] - v33);
        a1[3] = v31;
        a1[4] = v31 + 8 * v46;
        a1[5] = v31 + 8 * v29;
      }
      else
      {
        *v24 = v22;
        a1[4] += 8LL;
      }
      if ( (unsigned __int8)sub_1411919D0(v22, a2) == 0 )
        return 0;
      LOBYTE(v21) = v21 + 1;
    }
    while ( (unsigned __int8)v21 < v41 );
  }
  v34 = *a2;
  (*(void (__fastcall **)(_QWORD, char *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, &v42, 1);
  if ( *(_DWORD *)(v34 + 16) != 0 )
    return 0;
  if ( v42 != 0 )
  {
    v36 = sub_140F72AF0(104);
    sub_140F72BA0(v36);
    a1[6] = v36;
    if ( (unsigned __int16)qword_141B60330 <= 0xDDCu )
    {
      v37 = *a2;
      (*(void (__fastcall **)(_QWORD, char *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, &v43, 1);
      if ( *(_DWORD *)(v37 + 16) != 0 )
        return 0;
      v36 = a1[6];
    }
    if ( (unsigned __int8)sub_1415782C0(v36, a2) == 0 )
      return 0;
    if ( (unsigned __int16)qword_141B60330 <= 0xDDCu )
    {
      v38 = *a2;
      (*(void (__fastcall **)(_QWORD, char *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v49, 4);
      if ( *(_DWORD *)(v38 + 16) != 0 )
        return 0;
      v39 = *a2;
      (*(void (__fastcall **)(_QWORD, char *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v48, 4);
      if ( *(_DWORD *)(v39 + 16) != 0 )
        return 0;
      v40 = *a2;
      (*(void (__fastcall **)(_QWORD, char *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v47, 4);
      if ( *(_DWORD *)(v40 + 16) != 0 )
        return 0;
    }
  }
  return sub_140FAED40((_DWORD)a1, (_DWORD)a2, 0, a4, a5, a6, a7, a8);
}
