__int64 __fastcall sub_140823B40(__int64 a1, __int64 a2, unsigned int a3)
{
  __int64 v6; // rcx
  int v7; // r10d
  unsigned int *v8; // r9
  unsigned int *v9; // r11
  __int64 v10; // rax
  __int64 v11; // rbx
  bool v12; // dl
  bool v13; // dl
  __int64 v14; // rax
  __int64 v15; // r12
  __int64 v16; // rax
  int v17; // ecx
  __int64 v18; // r14
  __int64 v19; // rdi
  __int64 v20; // rdx
  BOOL v21; // esi
  __int64 *v22; // rbx
  __int64 v23; // rax
  unsigned int v24; // ecx
  __int64 *v25; // rdx
  __int64 v26; // rax
  __int64 v27; // rax
  __int64 *v29; // [rsp+28h] [rbp-28h] BYREF
  BOOL v30; // [rsp+30h] [rbp-20h]
  __int64 v31; // [rsp+38h] [rbp-18h]
  __int64 v32; // [rsp+40h] [rbp-10h]
  __int64 v33; // [rsp+48h] [rbp-8h]
  __int64 v34; // [rsp+50h] [rbp+0h]

  v34 = -2;
  v6 = *(_QWORD *)(a1 + 8);
  v7 = *(_DWORD *)(v6 + 268);
  v8 = *(unsigned int **)(v6 + 80);
  v9 = v8;
  if ( (__int64)(*(_QWORD *)(v6 + 88) - (_QWORD)v8) > 0 )
  {
    v10 = (*(_QWORD *)(v6 + 88) - (_QWORD)v8) >> 4;
    v9 = *(unsigned int **)(v6 + 80);
    v11 = v10;
    do
    {
      v11 = (unsigned __int64)v11 >> 1;
      v12 = v9[4 * v11] < a3;
      if ( v9[4 * v11] == a3 )
        v12 = (int)v9[4 * v11 + 1] < v7;
      if ( v12 )
      {
        v9 += 4 * v11 + 4;
        v11 = v10 + ~v11;
      }
      v10 = v11;
    }
    while ( v11 > 0 );
  }
  if ( v9 == *(unsigned int **)(v6 + 88) )
    goto LABEL_42;
  v13 = *v9 > a3;
  if ( *v9 == a3 )
    v13 = v7 < (int)v9[1];
  if ( v13 )
  {
LABEL_42:
    if ( v7 == 1 || v9 == v8 || (v14 = -1, *(v9 - 4) != a3) )
    {
      v33 = v6 + 208;
      MEMORY[0x141947418](v6 + 208);
      v15 = 0;
      goto LABEL_34;
    }
  }
  else
  {
    v14 = 0;
  }
  v15 = *(_QWORD *)&v9[4 * v14 + 2];
  v33 = v6 + 208;
  MEMORY[0x141947418](v6 + 208);
  if ( v15 == 0 )
  {
    v15 = 0;
    goto LABEL_34;
  }
  v16 = *(_QWORD *)(a1 + 8);
  v17 = *(_DWORD *)(v16 + 272);
  ++*(_WORD *)(v16 + 272);
  *(_WORD *)(v15 + 28) = v17;
  if ( *(_QWORD *)(v15 + 8) == *(_QWORD *)v15 )
  {
    v32 = v33;
    sub_140823E70(a1, v15);
  }
  v18 = *(_QWORD *)(a1 + 8);
  if ( (*(_BYTE *)(v18 + 264) & 4) != 0 )
  {
    v19 = *(_QWORD *)(v18 + 168);
    v20 = *(_QWORD *)(v19 + 8);
    v21 = false;
    if ( *(_BYTE *)(v20 + 25) != 0 )
    {
      v22 = *(__int64 **)(v19 + 8);
      v23 = *(_QWORD *)(v18 + 168);
      if ( *(_BYTE *)(v19 + 25) != 0 )
        goto LABEL_31;
    }
    else
    {
      v23 = *(_QWORD *)(v18 + 168);
      do
      {
        v22 = (__int64 *)v20;
        v24 = *(_DWORD *)(v20 + 28);
        v25 = (__int64 *)(v20 + 16);
        if ( v24 >= a3 )
        {
          v23 = (__int64)v22;
          v25 = v22;
        }
        v20 = *v25;
      }
      while ( *(_BYTE *)(v20 + 25) == 0 );
      v21 = v24 >= a3;
      if ( *(_BYTE *)(v23 + 25) != 0 )
        goto LABEL_31;
    }
    if ( *(_DWORD *)(v23 + 28) <= a3 )
    {
LABEL_33:
      ++*(_DWORD *)(v23 + 32);
      goto LABEL_34;
    }
LABEL_31:
    if ( *(_QWORD *)(v18 + 176) == 0x666666666666666LL )
    {
      v32 = v33;
      sub_140052D20();
    }
    v32 = v33;
    v26 = sub_141750CC0(40);
    *(_DWORD *)(v26 + 28) = a3;
    *(_DWORD *)(v26 + 32) = 0;
    *(_QWORD *)v26 = v19;
    *(_QWORD *)(v26 + 8) = v19;
    *(_QWORD *)(v26 + 16) = v19;
    *(_WORD *)(v26 + 24) = 0;
    v29 = v22;
    v30 = v21;
    v23 = sub_1407FAE70(v18 + 168, &v29, v26);
    goto LABEL_33;
  }
LABEL_34:
  *(_QWORD *)a2 = v15;
  *(_QWORD *)(a2 + 8) = 0;
  if ( (__int64 *)(a2 + 8) != &qword_141B59EE0 )
  {
    v27 = qword_141B59EE0;
    if ( qword_141B59EE0 != 0 )
      _InterlockedIncrement((volatile signed __int32 *)(qword_141B59EE0 - 4));
    *(_QWORD *)(a2 + 8) = v27;
  }
  v31 = a2 + 8;
  *(_QWORD *)(a2 + 16) = 0;
  *(_DWORD *)(a2 + 24) = a3;
  *(_BYTE *)(a2 + 28) = -1;
  sub_14081C770(a2);
  MEMORY[0x141947608](v33);
  return a2;
}
