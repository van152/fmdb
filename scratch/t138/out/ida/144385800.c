bool __fastcall sub_144385800(__int64 *a1, _QWORD *a2)
{
  __int64 v4; // rsi
  char v6; // r14
  __int64 v7; // rbx
  __int64 v8; // rsi
  __int64 v9; // rsi
  __int64 *v10; // rsi
  __int64 v11; // rbp
  unsigned __int64 v12; // rax
  unsigned __int64 v13; // r15
  unsigned __int64 v14; // rcx
  unsigned __int64 v15; // r15
  __int64 v16; // rdi
  __int64 *v17; // rbx
  __int64 v18; // rbx
  unsigned __int64 v19; // rcx
  __int64 v20; // rbp
  __int64 v21; // rsi
  char v22; // [rsp+26h] [rbp-52h] BYREF
  char v23; // [rsp+27h] [rbp-51h] BYREF
  int v24; // [rsp+28h] [rbp-50h] BYREF
  unsigned __int64 v25; // [rsp+30h] [rbp-48h]

  v22 = 0;
  v4 = *a2;
  (*(void (__fastcall **)(_QWORD, char *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v22, a3: 1);
  if ( *(_DWORD *)(v4 + 16) != 0 )
    return false;
  if ( v22 > 0 )
  {
    v6 = 0;
    while ( 1 )
    {
      v7 = sub_141750CC0(a1: 16);
      *(_QWORD *)v7 = 0;
      *(_DWORD *)(v7 + 8) = 0;
      v23 = 0;
      v8 = *a2;
      (*(void (__fastcall **)(_QWORD, char *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v23, a3: 1);
      if ( *(_DWORD *)(v8 + 16) != 0 )
        return false;
      sub_140814B10(a1: *a2, a2: &v24, a3: v7);
      if ( v24 != 0 )
        return false;
      v9 = *a2;
      (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v7 + 8, a3: 4);
      if ( *(_DWORD *)(v9 + 16) != 0 || *(_DWORD *)(*a2 + 16LL) != 0 )
        return false;
      v10 = (__int64 *)a1[1];
      if ( v10 == (__int64 *)a1[2] )
        break;
      *v10 = v7;
      a1[1] += 8;
LABEL_6:
      if ( ++v6 >= v22 )
        return *(_DWORD *)(*a2 + 16LL) == 0;
    }
    v11 = (__int64)v10 - *a1;
    v12 = v11 >> 3;
    v13 = (unsigned __int64)(v11 >> 3) >> 1;
    v14 = 0x1FFFFFFFFFFFFFFFLL - v13;
    v15 = (v11 >> 3) + v13;
    v25 = (v11 >> 3) + 1;
    if ( v15 <= v25 )
      v15 = v12 + 1;
    if ( v12 > v14 )
      v15 = 0x1FFFFFFFFFFFFFFFLL;
    v16 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v15);
    *(_QWORD *)(v16 + v11) = v7;
    v17 = (__int64 *)a1[1];
    sub_141758A00(a1: v16, a2: *a1, a3: (char *)v10 - *a1);
    if ( v17 != v10 )
      sub_141758A00(a1: v16 + v11 + 8, a2: v10, a3: a1[1] - (_QWORD)v10);
    v18 = *a1;
    if ( *a1 == 0 )
    {
LABEL_29:
      *a1 = v16;
      a1[1] = v16 + 8 * v25;
      a1[2] = v16 + 8 * v15;
      goto LABEL_6;
    }
    v19 = a1[2] - v18;
    if ( v19 == -1 )
    {
      v19 = *(unsigned int *)(v18 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
      {
LABEL_28:
        MEMORY[0x141948990](a1: v18 - *(unsigned int *)(qword_141ABD470 + 48));
        goto LABEL_29;
      }
    }
    else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
      goto LABEL_28;
    }
    v20 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v20) >> 3 > v19 )
    {
      v21 = *(_QWORD *)(v20 + 8 * v19);
      if ( v21 != 0 )
      {
        MEMORY[0x1419475D8](a1: v21 + 32, a2: v18 - *(unsigned int *)(v21 + 120));
        if ( (*(_BYTE *)(v21 + 72) == 0 || _InterlockedDecrement((volatile signed __int32 *)(v21 + 64)) == 0)
          && *(_BYTE *)(v21 + 97) != 0 )
        {
          sub_1412D33C0(a1: v21);
        }
        goto LABEL_29;
      }
    }
    goto LABEL_28;
  }
  return *(_DWORD *)(*a2 + 16LL) == 0;
}
