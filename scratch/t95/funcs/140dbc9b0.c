// THUNK ALIAS -> sub_143B53590 (jmp:0x140dbc9b0->0x143b53590)
__int64 __fastcall sub_143B53590(__int64 a1, __int64 a2)
{
  __int64 v3; // rdx

  *(_QWORD *)a1 = 0x141759DF8LL;
  *(_BYTE *)(a1 + 8) = 32;
  LOBYTE(a2) = 32;
  sub_1412EA280(a1 + 16, a2);
  LOBYTE(v3) = 32;
  sub_1412EB230(a1 + 32, v3);
  *(_QWORD *)a1 = 0x141876208LL;
  *(_QWORD *)(a1 + 16) = 0x1418762E8LL;
  *(_QWORD *)(a1 + 32) = 0x141876308LL;
  return a1;
}
