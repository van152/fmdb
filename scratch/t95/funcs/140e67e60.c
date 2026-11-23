// THUNK ALIAS -> sub_143C38E70 (jmp:0x140e67e60->0x143c38e70)
__int64 __fastcall sub_143C38E70(_QWORD *a1, char a2)
{
  __int64 v3; // rax

  if ( a1[3] == a1[4] )
    return 0;
  v3 = sub_1411DC000(a1, 0, 0, 0, 1u, 0);
  if ( v3 == 0 )
    return 0;
  else
    return sub_1411A43E0(v3, a2);
}
