_DWORD *__fastcall sub_144325730(_DWORD *a1, _QWORD *a2, __int64 *a3)
{
  __int64 v6; // rsi
  __int64 v7; // r13
  __int64 v8; // rbp
  __int64 v9; // r14
  __int64 v10; // rbx
  unsigned __int64 v11; // rcx
  __int64 v12; // r8
  __int64 v13; // rcx
  __int64 v14; // rbx
  __int64 v15; // rcx
  bool v16; // al
  __int64 v17; // rbx
  unsigned int v19; // [rsp+24h] [rbp-64h] BYREF
  __int64 v20; // [rsp+28h] [rbp-60h]
  _QWORD v21[2]; // [rsp+30h] [rbp-58h] BYREF
  int v22; // [rsp+40h] [rbp-48h]

  v19 = 0;
  (*(void (__fastcall **)(_QWORD, unsigned int *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v19, a3: 4);
  v6 = v19;
  if ( qword_141AA7808 <= (unsigned __int64)v19 )
  {
LABEL_20:
    *a1 = 1;
    return a1;
  }
  v7 = *a3;
  if ( 0xCCCCCCCCCCCCCCCDuLL * ((a3[2] - *a3) >> 2) < v19 )
  {
    v8 = a3[1];
    v9 = sub_1407E4490(a1: qword_141ABD470, a2: 20LL * v19);
    sub_141758A00(a1: v9, a2: *a3, a3: a3[1] - *a3);
    v10 = *a3;
    if ( *a3 == 0 )
    {
LABEL_13:
      *a3 = v9;
      a3[1] = v9 + v8 - v7;
      a3[2] = v9 + 20 * v6;
      LODWORD(v6) = v19;
      goto LABEL_14;
    }
    v11 = a3[2] - v10;
    if ( v11 == -1 )
    {
      v11 = *(unsigned int *)(v10 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
      {
LABEL_12:
        MEMORY[0x141948990](a1: v10 - *(unsigned int *)(qword_141ABD470 + 48));
        goto LABEL_13;
      }
    }
    else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
      goto LABEL_12;
    }
    v12 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v12) >> 3 > v11 )
    {
      v13 = *(_QWORD *)(v12 + 8 * v11);
      if ( v13 != 0 )
      {
        v14 = v10 - *(unsigned int *)(v13 + 120);
        v20 = v13;
        MEMORY[0x1419475D8](a1: v13 + 32, a2: v14);
        v15 = v20;
        v16 = *(_BYTE *)(v20 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v20 + 64)) != 0;
        if ( !v16 && *(_BYTE *)(v15 + 97) != 0 )
          sub_1412D33C0(a1: v15);
        goto LABEL_13;
      }
    }
    goto LABEL_12;
  }
LABEL_14:
  if ( (_DWORD)v6 != 0 )
  {
    v17 = 0;
    while ( 1 )
    {
      v22 = 0;
      v21[0] = -1;
      v21[1] = 0;
      if ( (unsigned __int8)sub_141727530(a1: v21, a2) == 0 )
        goto LABEL_20;
      if ( *(_DWORD *)(*a2 + 16LL) == 0 )
      {
        sub_140D03650(a1: a3, a2: v21);
        if ( ++v17 < (unsigned __int64)v19 )
          continue;
      }
      break;
    }
  }
  *a1 = *(_DWORD *)(*a2 + 16LL);
  return a1;
}
