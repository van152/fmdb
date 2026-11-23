__int64 __fastcall sub_143FC5B80(_QWORD *a1)
{
  _QWORD *v2; // r14
  _QWORD *v3; // rdi
  _QWORD *v4; // rsi
  __int64 v5; // rbx
  __int64 v6; // rbx
  __int64 result; // rax
  _QWORD *v8; // rbx
  _QWORD *v9; // r14
  _QWORD *v10; // rsi
  __int64 v11; // rbx
  __int64 v12; // rbx

  v2 = (_QWORD *)a1[3];
  v3 = (_QWORD *)a1[4];
  if ( v2 != v3 )
  {
    v4 = (_QWORD *)a1[3];
    do
    {
      v5 = *v4;
      if ( *v4 != 0 )
      {
        sub_141191740(*v4);
        sub_140FB07F0(v5);
      }
      ++v4;
    }
    while ( v4 != v3 );
    v6 = a1[4] - (_QWORD)v3;
    result = sub_141758A00(v2, v3, v6);
    v8 = (_QWORD *)((char *)v2 + v6);
    a1[4] = v8;
    v3 = v8;
  }
  if ( a1[6] != 0 )
  {
    result = sub_140FB0F20();
    v3 = (_QWORD *)a1[4];
  }
  a1[6] = 0;
  v9 = (_QWORD *)a1[3];
  if ( v9 != v3 )
  {
    v10 = (_QWORD *)a1[3];
    do
    {
      v11 = *v10;
      if ( *v10 != 0 )
      {
        sub_141191740(*v10);
        sub_140FB07F0(v11);
      }
      ++v10;
    }
    while ( v10 != v3 );
    v12 = a1[4] - (_QWORD)v3;
    result = sub_141758A00(v9, v3, v12);
    a1[4] = (char *)v9 + v12;
  }
  return result;
}
