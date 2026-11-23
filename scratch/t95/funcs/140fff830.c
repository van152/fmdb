// THUNK ALIAS -> sub_143E6D8E0 (jmp:0x140fff830->0x143e6d8e0)
__int64 *__fastcall sub_143E6D8E0(__int64 a1, __int64 *a2)
{
  __int64 **v3; // rax
  __int64 *v4; // rsi
  __int64 *v5; // rax
  _QWORD *v6; // rdi
  __int64 v7; // r13
  __int64 v8; // rbx
  unsigned __int64 v9; // rax
  unsigned __int64 v10; // r14
  unsigned __int64 v11; // rcx
  unsigned __int64 v12; // r14
  __int64 v13; // r15
  _QWORD *v14; // r13
  __int64 v15; // rdi
  unsigned __int64 v16; // rcx
  __int64 v17; // rbx
  __int64 v18; // rbx
  __int64 v20; // [rsp+20h] [rbp-58h]
  __int64 *v21; // [rsp+28h] [rbp-50h]
  unsigned __int64 v22; // [rsp+30h] [rbp-48h]

  v3 = *(__int64 ***)(qword_141B5FE58 + 128);
  v4 = *v3;
  v5 = v3[1];
  if ( v4 != v5 )
  {
    v21 = v5;
    v20 = a1;
    while ( 1 )
    {
      v7 = *v4;
      if ( *(_QWORD *)(*v4 + 64) == a1 || *(_QWORD *)(v7 + 72) == a1 )
      {
        v6 = (_QWORD *)a2[1];
        if ( v6 == (_QWORD *)a2[2] )
          break;
        *v6 = v7;
        a2[1] += 8;
      }
LABEL_5:
      if ( ++v4 == v5 )
        return a2;
    }
    v8 = (__int64)v6 - *a2;
    v9 = v8 >> 3;
    v10 = (unsigned __int64)(v8 >> 3) >> 1;
    v11 = 0x1FFFFFFFFFFFFFFFLL - v10;
    v12 = (v8 >> 3) + v10;
    v22 = (v8 >> 3) + 1;
    if ( v12 <= v22 )
      v12 = v9 + 1;
    if ( v9 > v11 )
      v12 = 0x1FFFFFFFFFFFFFFFLL;
    v13 = sub_1407E4490(qword_141ABD470, 8 * v12);
    *(_QWORD *)(v13 + v8) = v7;
    v14 = (_QWORD *)a2[1];
    sub_141758A00();
    if ( v14 != v6 )
      sub_141758A00();
    v15 = *a2;
    if ( *a2 == 0 )
    {
LABEL_26:
      *a2 = v13;
      a2[1] = v13 + 8 * v22;
      a2[2] = v13 + 8 * v12;
      v5 = v21;
      a1 = v20;
      goto LABEL_5;
    }
    v16 = a2[2] - v15;
    if ( v16 == -1 )
    {
      v16 = *(unsigned int *)(v15 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
      {
LABEL_25:
        MEMORY[0x141948990](v15 - *(unsigned int *)(qword_141ABD470 + 48));
        goto LABEL_26;
      }
    }
    else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
      goto LABEL_25;
    }
    v17 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v17) >> 3 > v16 )
    {
      v18 = *(_QWORD *)(v17 + 8 * v16);
      if ( v18 != 0 )
      {
        MEMORY[0x1419475D8](v18 + 32, v15 - *(unsigned int *)(v18 + 120));
        if ( (*(_BYTE *)(v18 + 72) == 0 || _InterlockedDecrement((volatile signed __int32 *)(v18 + 64)) == 0)
          && *(_BYTE *)(v18 + 97) != 0 )
        {
          sub_1412D33C0(v18);
        }
        goto LABEL_26;
      }
    }
    goto LABEL_25;
  }
  return a2;
}
