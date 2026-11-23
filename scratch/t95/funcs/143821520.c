unsigned __int64 __fastcall sub_143821520(__int64 *a1, unsigned __int64 *a2)
{
  unsigned __int64 *v4; // rbx
  unsigned __int64 result; // rax
  __int64 v6; // rdi
  unsigned __int64 v7; // rax
  unsigned __int64 v8; // r13
  unsigned __int64 v9; // r12
  unsigned __int64 v10; // rdx
  unsigned __int64 v11; // r12
  __int64 v12; // r14
  unsigned __int64 *v13; // r15
  __int64 v14; // rdi
  unsigned __int64 v15; // rcx
  __int64 v16; // rbx
  __int64 v17; // rbx
  bool v18; // al

  v4 = (unsigned __int64 *)a1[1];
  if ( v4 != (unsigned __int64 *)a1[2] )
  {
    result = *a2;
    *v4 = *a2;
    a1[1] += 8;
    return result;
  }
  v6 = (__int64)v4 - *a1;
  v7 = v6 >> 3;
  v8 = (v6 >> 3) + 1;
  v9 = (unsigned __int64)(v6 >> 3) >> 1;
  v10 = 0x1FFFFFFFFFFFFFFFLL - v9;
  v11 = (v6 >> 3) + v9;
  if ( v11 <= v8 )
    v11 = v7 + 1;
  if ( v7 > v10 )
    v11 = 0x1FFFFFFFFFFFFFFFLL;
  v12 = sub_1407E4490(qword_141ABD470, 8 * v11);
  *(_QWORD *)(v12 + v6) = *a2;
  v13 = (unsigned __int64 *)a1[1];
  sub_141758A00();
  if ( v13 != v4 )
    sub_141758A00();
  v14 = *a1;
  if ( *a1 != 0 )
  {
    v15 = a1[2] - v14;
    if ( v15 == -1 )
    {
      v15 = *(unsigned int *)(v14 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
      {
LABEL_18:
        MEMORY[0x141948990](v14 - *(unsigned int *)(qword_141ABD470 + 48));
        goto LABEL_19;
      }
    }
    else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
      goto LABEL_18;
    }
    v16 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v16) >> 3 > v15 )
    {
      v17 = *(_QWORD *)(v16 + 8 * v15);
      if ( v17 != 0 )
      {
        MEMORY[0x1419475D8](v17 + 32, v14 - *(unsigned int *)(v17 + 120));
        v18 = *(_BYTE *)(v17 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v17 + 64)) != 0;
        if ( !v18 && *(_BYTE *)(v17 + 97) != 0 )
          sub_1412D33C0(v17);
        goto LABEL_19;
      }
    }
    goto LABEL_18;
  }
LABEL_19:
  *a1 = v12;
  a1[1] = v12 + 8 * v8;
  result = v12 + 8 * v11;
  a1[2] = result;
  return result;
}
