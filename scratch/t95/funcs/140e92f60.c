// THUNK ALIAS -> sub_143C58280 (jmp:0x140e92f60->0x143c58280)
__int64 __fastcall sub_143C58280(__int64 *a1, __int64 *a2, int a3)
{
  __int64 v3; // rdx
  unsigned int v4; // esi
  int v5; // ecx
  __int64 v6; // rax
  _QWORD *v7; // rax
  __int64 v8; // rdi
  __int64 v9; // rbx
  bool v10; // zf

  if ( a1 == a2 )
    LODWORD(v3) = 0;
  else
    v3 = *a1;
  v4 = 0;
  v5 = a3;
  LOBYTE(a3) = -1;
  v6 = sub_140B5B8A0(v5, v3, a3, 0, 255);
  if ( v6 != 0 )
  {
    v7 = *(_QWORD **)(v6 + 88);
    if ( v7 == nullptr )
      return 0;
    v8 = v7[1];
    if ( *v7 == v8 )
    {
      return 0;
    }
    else
    {
      v9 = *v7 + 8LL;
      do
      {
        v4 = sub_140854570(*(_QWORD *)(v9 - 8));
        if ( (_BYTE)v4 != 0 )
          break;
        v10 = v9 == v8;
        v9 += 8;
      }
      while ( !v10 );
    }
  }
  return v4;
}
