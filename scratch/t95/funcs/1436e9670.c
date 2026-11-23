__int64 __fastcall sub_1436E9670(unsigned int **a1, __int64 a2, int a3, unsigned int a4, int a5)
{
  unsigned int *v8; // rax
  unsigned int v9; // r15d
  __int64 v10; // rcx
  int v11; // eax
  unsigned int *v12; // rdi
  int v13; // ebp
  int v14; // r12d
  unsigned int v15; // eax
  __int64 v16; // rcx

  v8 = *a1;
  if ( *a1 != nullptr )
    v9 = *v8;
  else
    v9 = 0;
  v10 = (__int64)(v8 + 1);
  if ( v8 == nullptr )
    v10 = 0x1419435F1LL;
  v11 = sub_140810720(v10, v9, a4);
  v12 = *a1;
  if ( *a1 == nullptr )
    return 0xFFFFFFFFLL;
  v13 = *v12;
  if ( *v12 == 0 )
    return 0xFFFFFFFFLL;
  v14 = v11;
  if ( v13 <= v11 )
    return 0xFFFFFFFFLL;
  if ( a3 == -1 )
  {
    a3 = sub_141758DB0(a2);
    if ( a3 == 0 )
      return 0xFFFFFFFFLL;
  }
  else if ( a3 == 0 )
  {
    return 0xFFFFFFFFLL;
  }
  if ( a3 > v13 )
    return 0xFFFFFFFFLL;
  v15 = sub_140810B50((int)v12 + 4, v13, v14, a2, a3, a5);
  if ( v15 == -1 )
    return 0xFFFFFFFFLL;
  v16 = (__int64)(*a1 + 1);
  if ( *a1 == nullptr )
    v16 = 0x1419435F1LL;
  return sub_1408105F0(v16, v9, v15);
}
