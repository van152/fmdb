// THUNK ALIAS -> sub_143877D10 (jmp:0x140932c50->0x143877d10)
char __fastcall sub_143877D10(__int64 a1)
{
  int v1; // eax

  v1 = *(unsigned __int8 *)(a1 + 572);
  if ( (unsigned int)(v1 - 105) < 6 || v1 == 8 )
    return 1;
  else
    return sub_1409D5090();
}
