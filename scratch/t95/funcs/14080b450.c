// THUNK ALIAS -> sub_1436EB3A0 (jmp:0x14080b450->0x1436eb3a0)
__int64 __fastcall sub_1436EB3A0(__int64 *a1)
{
  __int64 v1; // r8
  __int64 result; // rax
  char v3; // dl
  char *v4; // r8

  v1 = *a1;
  result = 0;
  if ( *a1 != 0 && *(int *)v1 > 0 )
  {
    v3 = *(_BYTE *)(v1 + 4);
    if ( v3 != 0 )
    {
      v4 = (char *)(v1 + 5);
      LODWORD(result) = 0;
      do
      {
        result = ((v3 & 0xC0) != 0x80) + (unsigned int)result;
        v3 = *v4++;
      }
      while ( v3 != 0 );
    }
  }
  return result;
}
