// THUNK ALIAS -> sub_143CA2A20 (jmp:0x140ec9b80->0x143ca2a20)
__int64 __fastcall sub_143CA2A20(_QWORD *a1)
{
  __int64 v2; // rcx
  __int64 v3; // rax
  unsigned __int64 v4; // rcx
  _QWORD **v5; // rax
  _QWORD *v6; // rcx
  _QWORD *v7; // rdi

  v2 = a1[3];
  if ( v2 != 0 )
  {
    if ( (unsigned __int64)(a1[5] - v2) >= 0x1000 )
    {
      v3 = *(_QWORD *)(v2 - 8);
      v4 = v2 - 8 - v3;
      if ( v4 >= 0x20 )
        MEMORY[0x1419488E8](v4);
      v2 = v3;
    }
    sub_141750D04(v2);
    a1[5] = 0;
    a1[4] = 0;
    a1[3] = 0;
  }
  v5 = (_QWORD **)a1[1];
  *v5[1] = 0;
  v6 = *v5;
  if ( *v5 != nullptr )
  {
    do
    {
      v7 = (_QWORD *)*v6;
      sub_141750D04(v6);
      v6 = v7;
    }
    while ( v7 != nullptr );
  }
  return sub_141750D04(a1[1]);
}
