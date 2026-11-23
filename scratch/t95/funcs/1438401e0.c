char __fastcall sub_1438401E0(__int64 *a1, _QWORD *a2)
{
  _QWORD *v4; // rbx
  __int64 v5; // rax
  __int64 v6; // rsi
  unsigned __int64 v7; // rax
  unsigned __int64 v8; // r13
  unsigned __int64 v9; // r12
  unsigned __int64 v10; // rdx
  unsigned __int64 v11; // r12
  __int64 v12; // r12
  __int64 v13; // r14
  __int64 v14; // rcx
  _QWORD *v15; // rdi
  __int64 v16; // rdi
  unsigned __int64 v17; // rcx
  __int64 v18; // rbx
  __int64 v19; // rsi

  v4 = (_QWORD *)a1[1];
  if ( v4 == (_QWORD *)a1[2] )
  {
    v6 = (__int64)v4 - *a1;
    v7 = v6 >> 4;
    v8 = (v6 >> 4) + 1;
    v9 = (unsigned __int64)(v6 >> 4) >> 1;
    v10 = 0xFFFFFFFFFFFFFFFLL - v9;
    v11 = (v6 >> 4) + v9;
    if ( v11 <= v8 )
      v11 = v7 + 1;
    if ( v7 > v10 )
      v11 = 0xFFFFFFFFFFFFFFFLL;
    v12 = 16 * v11;
    v13 = sub_1407E4490(qword_141ABD470, v12);
    v14 = a2[1];
    *(_QWORD *)(v13 + v6) = *a2;
    *(_QWORD *)(v13 + v6 + 8) = v14;
    v15 = (_QWORD *)a1[1];
    LOBYTE(v5) = sub_141758A00();
    if ( v15 != v4 )
      LOBYTE(v5) = sub_141758A00();
    v16 = *a1;
    if ( *a1 == 0 )
      goto LABEL_19;
    v17 = a1[2] - v16;
    if ( v17 == -1 )
    {
      v17 = *(unsigned int *)(v16 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
        goto LABEL_18;
    }
    else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
      goto LABEL_18;
    }
    v18 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v18) >> 3 > v17 )
    {
      v19 = *(_QWORD *)(v18 + 8 * v17);
      if ( v19 != 0 )
      {
        MEMORY[0x1419475D8](v19 + 32, v16 - *(unsigned int *)(v19 + 120));
        LOBYTE(v5) = *(_BYTE *)(v19 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v19 + 64)) != 0;
        if ( (_BYTE)v5 == 0 && *(_BYTE *)(v19 + 97) != 0 )
          LOBYTE(v5) = sub_1412D33C0(v19);
        goto LABEL_19;
      }
    }
LABEL_18:
    LOBYTE(v5) = MEMORY[0x141948990](v16 - *(unsigned int *)(qword_141ABD470 + 48));
LABEL_19:
    *a1 = v13;
    a1[1] = v13 + 16 * v8;
    a1[2] = v13 + v12;
    return v5;
  }
  v5 = *a2;
  v4[1] = a2[1];
  *v4 = v5;
  a1[1] += 16;
  return v5;
}
