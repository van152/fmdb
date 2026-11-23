bool __fastcall sub_141726770(__int64 *a1, _QWORD *a2)
{
  _QWORD *v2; // r15
  __int64 v4; // rsi
  __int64 v6; // rbp
  __int64 v7; // r12
  __int64 v8; // rsi
  __int64 v9; // r13
  __int64 v10; // rbx
  unsigned __int64 v11; // rcx
  __int64 v12; // r8
  __int64 v13; // rdi
  bool v14; // al
  __int64 v15; // rbp
  _QWORD *v16; // rsi
  __int64 v17; // rbx
  unsigned __int64 v18; // rax
  unsigned __int64 v19; // r13
  unsigned __int64 v20; // rcx
  unsigned __int64 v21; // r13
  __int64 v22; // r12
  _QWORD *v23; // r15
  __int64 v24; // rsi
  unsigned __int64 v25; // rcx
  __int64 v26; // rbx
  __int64 v27; // rbx
  unsigned int v28; // [rsp+2Ch] [rbp-5Ch] BYREF
  __int64 v29; // [rsp+30h] [rbp-58h] BYREF
  _QWORD *v30; // [rsp+38h] [rbp-50h]
  unsigned __int64 v31; // [rsp+40h] [rbp-48h]

  v2 = a2;
  if ( *a1 != a1[1] )
    a1[1] = *a1;
  v28 = 0;
  v4 = *a2;
  (*(void (__fastcall **)(_QWORD, unsigned int *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, &v28, 4);
  if ( *(_DWORD *)(v4 + 16) != 0 )
    return false;
  v6 = v28;
  v7 = *a1;
  if ( (a1[2] - *a1) >> 3 < (unsigned __int64)v28 )
  {
    v8 = a1[1];
    v9 = sub_1407E4490(qword_141ABD470, 8LL * v28);
    sub_141758A00(v9, *a1, a1[1] - *a1);
    v10 = *a1;
    if ( *a1 != 0 )
    {
      v11 = a1[2] - v10;
      if ( v11 == -1 )
        v11 = *(unsigned int *)(v10 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
        && (v12 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v12) >> 3 > v11)
        && (v13 = *(_QWORD *)(v12 + 8 * v11)) != 0 )
      {
        MEMORY[0x1419475D8](v13 + 32, v10 - *(unsigned int *)(v13 + 120));
        v14 = *(_BYTE *)(v13 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v13 + 64)) != 0;
        if ( !v14 && *(_BYTE *)(v13 + 97) != 0 )
          sub_1412D33C0(v13);
      }
      else
      {
        MEMORY[0x141948990](v10 - *(unsigned int *)(qword_141ABD470 + 48));
      }
    }
    *a1 = v9;
    a1[1] = v9 + v8 - v7;
    a1[2] = v9 + 8 * v6;
    LODWORD(v6) = v28;
  }
  if ( (_DWORD)v6 != 0 )
  {
    v15 = 0;
    v30 = v2;
    while ( 1 )
    {
      v29 = 0;
      if ( (unsigned __int8)sub_140F83A50(&v29, v2) == 0 )
        return false;
      v16 = (_QWORD *)a1[1];
      if ( v16 == (_QWORD *)a1[2] )
        break;
      *v16 = v29;
      a1[1] += 8;
LABEL_19:
      if ( ++v15 >= (unsigned __int64)v28 )
        return *(_DWORD *)(*v2 + 16LL) == 0;
    }
    v17 = (__int64)v16 - *a1;
    v18 = v17 >> 3;
    v19 = (unsigned __int64)(v17 >> 3) >> 1;
    v20 = 0x1FFFFFFFFFFFFFFFLL - v19;
    v21 = (v17 >> 3) + v19;
    v31 = (v17 >> 3) + 1;
    if ( v21 <= v31 )
      v21 = v18 + 1;
    if ( v18 > v20 )
      v21 = 0x1FFFFFFFFFFFFFFFLL;
    v22 = sub_1407E4490(qword_141ABD470, 8 * v21);
    *(_QWORD *)(v22 + v17) = v29;
    v23 = (_QWORD *)a1[1];
    sub_141758A00(v22, *a1, (char *)v16 - *a1);
    if ( v23 != v16 )
      sub_141758A00(v22 + v17 + 8, v16, a1[1] - (_QWORD)v16);
    v24 = *a1;
    v2 = v30;
    if ( *a1 == 0 )
    {
LABEL_39:
      *a1 = v22;
      a1[1] = v22 + 8 * v31;
      a1[2] = v22 + 8 * v21;
      goto LABEL_19;
    }
    v25 = a1[2] - v24;
    if ( v25 == -1 )
    {
      v25 = *(unsigned int *)(v24 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
      {
LABEL_38:
        MEMORY[0x141948990](v24 - *(unsigned int *)(qword_141ABD470 + 48));
        goto LABEL_39;
      }
    }
    else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
      goto LABEL_38;
    }
    v26 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v26) >> 3 > v25 )
    {
      v27 = *(_QWORD *)(v26 + 8 * v25);
      if ( v27 != 0 )
      {
        MEMORY[0x1419475D8](v27 + 32, v24 - *(unsigned int *)(v27 + 120));
        if ( (*(_BYTE *)(v27 + 72) == 0 || _InterlockedDecrement((volatile signed __int32 *)(v27 + 64)) == 0)
          && *(_BYTE *)(v27 + 97) != 0 )
        {
          sub_1412D33C0(v27);
        }
        goto LABEL_39;
      }
    }
    goto LABEL_38;
  }
  return *(_DWORD *)(*v2 + 16LL) == 0;
}
