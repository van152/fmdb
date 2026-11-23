// THUNK ALIAS -> sub_1436720E0 (jmp:0x1407e49f0->0x1436720e0)
__int64 __fastcall sub_1436720E0(__int64 a1)
{
  __int64 v2; // rax
  __int64 *v3; // r14
  char *v4; // rbx
  char *v5; // rcx
  __int64 v6; // rdi
  char *v7; // rax
  __int64 result; // rax
  unsigned __int64 v9; // rcx
  char *v10; // rax

  *(_BYTE *)(a1 + 52) = 0;
  v2 = *(_QWORD *)(a1 + 24);
  if ( v2 != *(_QWORD *)(a1 + 32) )
    *(_QWORD *)(a1 + 32) = v2;
  v3 = (__int64 *)(a1 + 24);
  v4 = *(char **)a1;
  v5 = *(char **)(a1 + 8);
  if ( *(char **)a1 == v5 )
  {
    v5 = *(char **)a1;
  }
  else
  {
    do
    {
      v6 = *(_QWORD *)v4;
      if ( *(_QWORD *)v4 != 0 )
      {
        sub_1407E5170(*(_QWORD *)v4);
        sub_141750CFC(v6);
        v5 = *(char **)(a1 + 8);
      }
      v4 += 8;
    }
    while ( v4 != v5 );
    v7 = *(char **)a1;
    if ( *(char **)a1 != v5 )
    {
      *(_QWORD *)(a1 + 8) = v7;
      v5 = v7;
    }
  }
  result = *v3;
  if ( *v3 != 0 )
  {
    if ( (unsigned __int64)(*(_QWORD *)(a1 + 40) - result) >= 0x1000 )
    {
      v9 = *(_QWORD *)(result - 8);
      if ( result - 8 - v9 >= 0x20 )
        goto LABEL_21;
      result = *(_QWORD *)(result - 8);
    }
    result = sub_141750D04(result);
    *(_QWORD *)(a1 + 40) = 0;
    *(_QWORD *)(a1 + 32) = 0;
    *v3 = 0;
    v5 = *(char **)a1;
  }
  if ( v5 == nullptr )
    return result;
  if ( *(_QWORD *)(a1 + 16) - (_QWORD)v5 >= 0x1000u )
  {
    v10 = *((char **)v5 - 1);
    v9 = v5 - 8 - v10;
    if ( v9 < 0x20 )
    {
      v5 = v10;
      goto LABEL_19;
    }
LABEL_21:
    MEMORY[0x1419488E8](v9);
  }
LABEL_19:
  result = sub_141750D04(v5);
  *(_QWORD *)(a1 + 16) = 0;
  *(_QWORD *)(a1 + 8) = 0;
  *(_QWORD *)a1 = 0;
  return result;
}
